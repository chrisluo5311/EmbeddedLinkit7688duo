import time
import mraa
from RPLCD.i2c import CharLCD

# Initialize LCD
lcd = CharLCD('PCF8574', address=0x3F, port=1, backlight_enabled=True)

# Define keypad
BUTTONS = [
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
mraa.Gpio(BUZZER_PIN).dir(mraa.DIR_OUT)

def setup_buttons():
    buttons = [[mraa.Gpio(COL_PINS[col]) for col in range(len(COL_PINS))] for _ in range(len(ROW_PINS))]
    for row in range(len(ROW_PINS)):
        for col in range(len(COL_PINS)):
            buttons[row][col].dir(mraa.DIR_IN)
            buttons[row][col].mode(mraa.MODE_PULLUP)
    return buttons

def button_callback(row, col):
    global DATA, DATA_COUNT
    lcd.cursor_pos = (0, 0)
    lcd.write_string("Enter Password:")

    key = BUTTONS[row][col]
    DATA += key
    lcd.cursor_pos = (1, DATA_COUNT)
    lcd.write_string(key)
    DATA_COUNT += 1

    if DATA_COUNT == PASSWORD_LENGTH:
        lcd.clear()
        print("Password:", DATA)
        if DATA == MASTER_PASSWORD:
            lcd.write_string("Correct")
            mraa.Gpio(BUZZER_PIN).write(1)
            time.sleep(0.5)
            mraa.Gpio(BUZZER_PIN).write(0)
        else:
            lcd.write_string("Incorrect")
            mraa.Gpio(BUZZER_PIN).write(1)
            time.sleep(0.5)
            mraa.Gpio(BUZZER_PIN).write(0)

        lcd.clear()
        clear_data()

def clear_data():
    global DATA_COUNT, DATA
    DATA_COUNT = 0
    DATA = ""

buttons = setup_buttons()

try:
    while True:
        for row in range(len(ROW_PINS)):
            for col in range(len(COL_PINS)):
                if buttons[row][col].read() == 0:
                    button_callback(row, col)
                    time.sleep(0.2)  # debounce time
except KeyboardInterrupt:
    pass
finally:
    mraa.Gpio(BUZZER_PIN).write(0)