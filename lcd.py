import I2C_LCD_driver
import time

mylcd = I2C_LCD_driver.lcd()

# Test1
while True:
    mylcd.lcd_display_string("Developer", 1)
    mylcd.lcd_display_string("Dreamming!!", 2, 3)
    time.sleep(1)
    mylcd.lcd_clear()
    time.sleep(1)

# Test2
# while True:
#    mylcd.lcd_display_string("Time: %s" %time.strftime("%H:%M:%S"), 1)
#    mylcd.lcd_display_string("Date: %s" %time.strftime("%m/%d/%Y"), 2)


# Test3
# str_pad = " " * 16
# my_long_string = "Thank for subscribe the DeveloperDreamming!!!!!"
# my_long_string = str_pad + my_long_string
# while True:
#    for i in range (0, len(my_long_string)):
#        lcd_text = my_long_string[i:(i+16)]
#        mylcd.lcd_display_string(lcd_text,1)
#        sleep(0.4)
#        mylcd.lcd_display_string(str_pad,1)
