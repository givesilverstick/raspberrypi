import RPi.GPIO as GPIO
import I2C_LCD_driver
import time
import spidev
from subprocess import call
from datetime import datetime

# 드라이버 모터와 연결한 핀 번호 지정
IN1= 5
IN2 = 6
# ENA = 13
R = 16
G = 20
B = 21
btnPin = 22
shutdown_sec = 2

HUM_THRESHOLD = 20  # 습도(%) 임계치 (변경O)
HUM_MAX = 0         # 토양습도센서 출력 값

# GPIO 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(R, GPIO.OUT)
GPIO.setup(G, GPIO.OUT)
GPIO.setup(B, GPIO.OUT)
GPIO.setup(btnPin, GPIO.IN)
# GPIO.output(IN1, GPIO.LOW)
# GPIO.output(IN2, GPIO.LOW)
# GPIO.setup(ENA, GPIO.OUT)
# GPIO.output(ENA, GPIO.LOW)

# spi 설정
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 500000   # 모터 속도

# ADC 값을 가져오는 함수
def read_spi_adc(adcChannel):
    adcValue = 0
    buff = spi.xfer2([1,(8+adcChannel)<<4,0])
    adcValue = ((buff[1]&3)<<8)+buff[2]
    return adcValue

# 센서 값을 백분율로 변환하는 함수
def map(value, min_adc, max_adc, min_hum, max_hum):
    adc_range = max_adc - min_adc
    hum_range = max_hum - min_hum
    scale_factor = float(adc_range) / float(hum_range)
    return min_hum + ((value - min_adc) / scale_factor)

#
def getPressTime():
    elapsed = 0
    if pressTime is not None:
        elapsed = (datetime.now() - pressTime).total_seconds()
    return elapsed

try:
    strPer = "%"
    mylcd = I2C_LCD_driver.lcd()
    adcChannel = 0
    strCur = ""

    # 워터 펌프를 돌릴지 말지 결정하는 while문
    while True:
        input = GPIO.input(btnPin)
        prevInput = input
        if input == 0:
            if prevInput == -1 or prevInput == 1:
                pressTime = datetime.now()
            elif prevInput == 0:
                if getPressTime() >= shutdown_sec:
                    call(['shutdown', '-h', 'now'], shell=False)
                    break

        adcValue = read_spi_adc(adcChannel)
        hum = 100 - int(map(adcValue, HUM_MAX, 1023, 0, 100))   # 가져온 데이터를 % 단위로 변환, 습도가 높을수록 낮은 값을 반환 (100에서 뺀 이유)
        # 임계치보다 수분 값이 작을 경우, 워터 펌프 작동
        if hum < HUM_THRESHOLD:
            GPIO.output(IN1, GPIO.HIGH)
            GPIO.output(IN2, GPIO.LOW)
            GPIO.output(R, GPIO.HIGH)
            GPIO.output(G, GPIO.LOW)
            GPIO.output(B, GPIO.LOW)
            print('yes')
            strCur = "Warning"
        # 임계치보다 수분 값이 같거나 클 경우, 워터 펌프 작동 X
        else:
            GPIO.output(IN1, GPIO.LOW)
            GPIO.output(IN2, GPIO.LOW)
            GPIO.output(R, GPIO.LOW)
            GPIO.output(G, GPIO.HIGH)
            GPIO.output(B, GPIO.LOW)
            print('no')
            strCur = "Normal"

        mylcd.lcd_clear()
        mylcd.lcd_display_string("HUM:%d%s" % (hum, strPer), 1)
        mylcd.lcd_display_string("STATUS:%s" % strCur, 2)
        time.sleep(0.5)
finally:
    GPIO.cleanup()
    spi.close()
