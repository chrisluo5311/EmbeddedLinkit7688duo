import time
import RPi.GPIO as GPIO
from pad4pi import rpi_gpio
from RPLCD.i2c import CharLCD

# Initialize LCD
lcd = CharLCD('PCF8574AT', address=0x3F, port=1, backlight_enabled=True)

# Define keypad
KEYPAD = [
    ["1", "2", "3", "A"],
    ["4", "5", "6", "B"],
    ["7", "8", "9", "C"],
    ["*", "0", "#", "D"]
]

ROW_PINS = [5, 6, 7, 8]  # Row pins
COL_PINS = [9, 10, 11, 12]  # Column pins

# Password settings
PASSWORD_LENGTH = 7
MASTER_PASSWORD = "AD123*0"
DATA = ""
DATA_COUNT = 0

# Buzzer settings
BUZZER_PIN = 14
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(BUZZER_PIN, GPIO.LOW)

# Setup keypad
factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

# Callback function for key events
def key_callback(key):
    global DATA, DATA_COUNT
    lcd.cursor_pos = (0, 0)
    lcd.write_string("Enter Password:")
    
    DATA += key
    lcd.cursor_pos = (1, DATA_COUNT)
    lcd.write_string(key)
    DATA_COUNT += 1

    if DATA_COUNT == PASSWORD_LENGTH:
        lcd.clear()
        print("Password:", DATA)
        if DATA == MASTER_PASSWORD:
            lcd.write_string("Correct")
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(BUZZER_PIN, GPIO.LOW)
        else:
            lcd.write_string("Incorrect")
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(BUZZER_PIN, GPIO.LOW)

        lcd.clear()
        clear_data()

def clear_data():
    global DATA_COUNT, DATA
    DATA_COUNT = 0
    DATA = ""

# Assign callback function to key events
keypad.registerKeyPressHandler(key_callback)

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()