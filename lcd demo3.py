import I2C_LCD_driver
from time import*

mylcd = I2C_LCD_driver.lcd()


try:
    while True:
        mylcd.lcd_display_string("push the button", 1)  # Write line of text to first line of display
        mylcd.lcd_display_string("  * select * ", 2)  # Write line of text to second line of display
        sleep(2)
        mylcd.lcd_display_string("push the button", 1)                  # Give time for the message to be read
        mylcd.lcd_display_string("    select   ", 2)   # Refresh the first line of display with a different message
        sleep(2)                                           # Give time for the message to be read                                          # Give time for the message to be read
except KeyboardInterrupt:

    print("???")
    mylcd.lcd_clear()