# Employee access control system with Linkit7688duo

<div>
<img src="https://img.shields.io/badge/Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white">
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/HTML-239120?style=for-the-badge&logo=html5&logoColor=white">
<img src="https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=Raspberry%20Pi&logoColor=white">
</div>

---

<h2 ><img src="https://img.icons8.com/office/30/000000/training.png"/> &nbspProject Introduction and Objectives: </h2>

### Control and manage personnel entering and exiting a specific area to ensure the safety of the area and protect property.


|    System     | Introduction                                                                                   | 
|:-------------:|:-----------------------------------------------------------------------------------------------|
|   End User    | The employee uses the Keypad to enter the password, and the password is displayed on the LCD screen. If the password is wrong, the buzzer will sound for 0.5 seconds as a reminder and "Incorrect" word will be displayed on the LCD screen. If the password is correct, "Correct" word will be displayed on the LCD screen. |
| Administrator | Administrators can monitor the person who enters the password by browsing the real-time image screen through the video streaming service on the web interface. You can also use the on/off input keys of the web interface to sound the buzzer to drive away criminals. |

---

<h2>Software version:</h2>

| Software | Version |
|:--------:|:--------|
|Arduino IDE| 1.6.5   |
|Adafruit_Keypad| 1.3.2   |
|Wire| 1.0.0   |
|LiquidCrystal_I2C| 1.1.2   |
|Python| 2.7     |

---
<h2>Figure:</h2>

<img src="https://github.com/chrisluo5311/EmbeddedLinkit7688duo/blob/main/static/Figure1.jpg" width="600">
<img src="https://github.com/chrisluo5311/EmbeddedLinkit7688duo/blob/main/static/Figure2.jpg" width="600">


---
<h2>Component Diagram:</h2>
<img src="https://github.com/chrisluo5311/EmbeddedLinkit7688duo/blob/main/static/component_diagram.jpg" width="600">



- Raspberry Pi 400:
<img src="https://github.com/chrisluo5311/EmbeddedLinkit7688duo/blob/main/static/pi400.jpg" width="300">

- LCD1602 I2C:
<img src="https://github.com/chrisluo5311/EmbeddedLinkit7688duo/blob/main/static/LCDI2C.jpg" width="300">
  
- Keypad: 4*4
<img src="https://github.com/chrisluo5311/EmbeddedLinkit7688duo/blob/main/static/keypad.jpg" width="300">

- LED:
<img src="https://github.com/chrisluo5311/EmbeddedLinkit7688duo/blob/main/static/LED.jpg" width="200">

- Active Buzzer
<img src="https://github.com/chrisluo5311/EmbeddedLinkit7688duo/blob/main/static/activebuzzer.jpg" width="300">
  
- Webcam: RAZER KIYO X
<img src="https://github.com/chrisluo5311/EmbeddedLinkit7688duo/blob/main/static/webcam.jpg" width="200">

---

<h2>Challenges</h2>

1. The hardware's built-in Python version is 2.7 with outdated pip and setup packages, preventing software package installations or updates. Many packages now require Python 3.0 or higher, so the built-in mraa library is used for control.
2. CGI Python's redirection to another webpage is cumbersome, requiring direct HTML structure printing. The webpage was later moved to a Raspberry Pi 400, with the Linkit 7688 Duo handling only data transmission.
3. The latest Arduino IDE version is incompatible with the MediaTek board. Installing a community-provided json and zip file in Arduino IDE version 1.6.5 resolved this issue.
4. Due to version constraints, the MQTT WiFi kit couldn't connect to a mobile hotspot. Instead, direct communication between Linkit Smart 7688duo and Pi400 was established for signal transmission. 


---
<h2>Keypad Code</h2>

```Arduino
#include "Adafruit_Keypad.h"
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x3F,16,2); 
const byte ROWS = 4; // ROW count
const byte COLS = 4; // Collumn count
//Define the name of each key on the keyboard
char keys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};
byte rowPins[ROWS] = {5, 6, 7, 8}; //Define the row pin
byte colPins[COLS] = {9, 10, 11, 12}; //Define the column pin

//Initialize the Keypad
Adafruit_Keypad customKeypad = Adafruit_Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS);

void setup() {
  pinMode(14, OUTPUT);
  
  digitalWrite(14, LOW);
  
  Serial.begin(9600);
  customKeypad.begin();
  Serial.println("KeyPad Test...");

  lcd.init();
  lcd.backlight();
}

void loop() {
  // Start detecting the user's keystroke status
  customKeypad.tick();

  //Determine which key was pressed
  while(customKeypad.available()){
    keypadEvent e = customKeypad.read();
    Serial.print((char)e.bit.KEY);
    if(e.bit.EVENT == KEY_JUST_PRESSED) {
      Serial.println(" pressed"); 
      char customkey = (char)e.bit.KEY;
      lcd.setCursor(0,0);
      lcd.print(customkey);
      if (customkey != '1') {
        digitalWrite(14, HIGH);
        delay(1000);
        digitalWrite(14, LOW);
        delay(1000); 
       }
    //The pressed state is KEY_JUST_PRESSED
    } else if (e.bit.EVENT == KEY_JUST_RELEASED) {
      Serial.println(" released");  
    //The released status is KEY_JUST_RELEASED
    }
  }

  delay(10);
}
```

<h2>Demo Code</h2>

```Python
from flask import Flask, request, render_template,redirect
import RPi.GPIO as GPIO
import time
app = Flask(__name__)

# Define ledPin
ledPin = 14
# Define testOutPin for input 7688 to control active buzzer
testOutPin = 15 

# Set ledpin & testOutPin to low at setup
def setup():
    GPIO.setmode(GPIO.BCM)       
    GPIO.setup(ledPin, GPIO.OUT)   
    GPIO.output(ledPin, GPIO.LOW)  
    
    GPIO.setup(testOutPin, GPIO.OUT)   
    GPIO.output(testOutPin, GPIO.LOW)  

# Ouput testOutPin HIGH to let the active buzzer sound
def sound():
    GPIO.output(ledPin, GPIO.HIGH)     # make ledPin output HIGH level to turn on led   
    GPIO.output(testOutPin, GPIO.HIGH) # make testOutPin output HIGH to let the active buzzer sound     
    print ('led,buzzer turned on >>>') # print information on terminal

# Make all pin out LOW to turn off LED & buzzer
def destroy():
    GPIO.output(ledPin, GPIO.LOW)      # set the ledPin to output LOW
    GPIO.output(testOutPin, GPIO.LOW)  # set the testOutPin to output LOW
    GPIO.cleanup()

@app.route("/")
def hello():
    return "Hello, World!"

# Redirect to form html to control buzzer and monitor
@app.route("/test")
def test():
    return render_template("flaskform.html")

# Send post to turn on led and let the buzzer sound 
@app.route("/blink",methods=["GET","POST"])
def blink():
    # Get form value
    islight = request.form.get("LED")
    if islight == "U":
        sound() # sound the buzzer & turn on LED
    else:
        destroy()
    return render_template("flaskform.html")
  
app.run()
```

<h2>HTML</h2>

```HTML
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Any kinds of test</title>
</head>
<body>
    <form method='post'action="{{ url_for("blink")}}">
        開起led燈泡和峰鳴器 :<br>
        <input type="radio" name="LED" value="U">ON<br>
        <input type="radio" name="LED" value="OFF">OFF<br>
        <input type="submit" value="Submit" />
    </form>
    <img src="http://192.168.43.205:8080/?action=stream">
</body>
</html>
```

<h2>Arduino</h2>

```Arduino
#include "Adafruit_Keypad.h"
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x3F,16,2); 
const byte ROWS = 4; // ROW count
const byte COLS = 4; // Collumn count

// Define the name of each key on the keyboard
char keys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};

byte rowPins[ROWS] = {5, 6, 7, 8};    //Define the row pin
byte colPins[COLS] = {9, 10, 11, 12}; //Define the column pin

//Initialize Keypad
Adafruit_Keypad customKeypad = Adafruit_Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS);


#define BuzzerPIN 14 
#define piPIN 16

// ##############
// ## password ##
// ##############

// Password Length
const int Password_Length = 7;
// Character to hold password input
String Data;

// Password
String Master = "AD123*0";

// Pin connected to lock relay signal
int lockOutput = 11;

// Counter for character entries
byte data_count = 0;

// Character to hold key input
char customKey;
// ##############

void setup() {
  // BuzzerPIN
  pinMode(BuzzerPIN, OUTPUT);
  digitalWrite(BuzzerPIN, LOW);

  pinMode(piPIN, INPUT_PULLUP); 
  
  Serial.begin(9600);
  customKeypad.begin();

  lcd.init();
  lcd.backlight();
}

void loop() {

  // Initialize LCD and print
  lcd.setCursor(0, 0);
  lcd.print("Enter Password:");

  customKeypad.tick();
  while (customKeypad.available())
  {
    // Enter keypress into array and increment counter
    keypadEvent e = customKeypad.read();
    customKey = (char)e.bit.KEY;
    if (e.bit.EVENT == KEY_JUST_RELEASED) {
      Data += customKey;
      lcd.setCursor(data_count, 1);
      lcd.print(Data[data_count]);
      data_count++;   
      break;
    }
  }
  

  // See if we have reached the password length
  if (data_count == Password_Length) {
    lcd.clear();
    Serial.println("Password: ");
    Serial.print(Data);

    if (Data == Master) {
      // Correct Password
      lcd.print("Correct");
      // Turn on relay for 5 seconds
      // digitalWrite(BuzzerPIN, HIGH);
      delay(500);
      // digitalWrite(BuzzerPIN, LOW);
    }
    else {
      // Incorrect Password
      lcd.print("Incorrect");
      digitalWrite(BuzzerPIN, HIGH);

      delay(500);
      digitalWrite(BuzzerPIN, LOW);

    }

    // Clear data and LCD display
    lcd.clear();
    clearData();
  }

  
  int piState = digitalRead(piPIN);
  Serial.println(piState);
  if (piState == HIGH){
      digitalWrite(BuzzerPIN, HIGH);   
      delay(100);
      digitalWrite(BuzzerPIN, LOW); 
    }
   else{
      digitalWrite(BuzzerPIN, LOW);
    }
}


void clearData() {
  //Reset data_count
  data_count = 0;
  //Reset Data
  Data ="";
}
```

<h2>Result Presentation:</h2>

<img src="https://github.com/chrisluo5311/EmbeddedLinkit7688duo/blob/main/static/Result1.jpg" width="400">

<img src="https://github.com/chrisluo5311/EmbeddedLinkit7688duo/blob/main/static/Result2.jpg" width="400">

Video Demo 1 : [webcam](https://youtu.be/uD_uT3pB8uw)

Video Demo 2 : [keypad](https://youtube.com/shorts/u9iraENu_ps)



---
<h2>PDF & PowerPoint </h2>

PDF : [pdf](https://github.com/chrisluo5311/EmbeddedLinkit7688duo/blob/main/static/ProcessGroup_4_Employee%20Access%20Control%20System.pdf)

PowerPoint: [powerpoint](https://github.com/chrisluo5311/EmbeddedLinkit7688duo/blob/main/static/Employee%20Access%20Control%20System%20%20Group%204.pdf)


---
<h2>Reference</h2>

|                           Name                           |        URL         |      Notes      |
|:--------------------------------------------------------:|:------------------:|:---------------:|
| How to find out which version of OpenWRT you are running |https://techoverflow.net/2023/02/26/how-to-find-out-which-version-of-openwrt-you-are-running/||
| html - Webpage redirect to the main page with CGI Python |https://stackoverflow.com/questions/6122957/webpage-redirect-to-the-main-page-with-cgi-python|How to redirect to another web page in CGI|
| Linkitsmart-7688 Duo interesting projects and references |https://lct4246.blogspot.com/2016/03/7688-duo-references.html||
|                    LCD I2C Operations                    |https://hackmd.io/@1KJngEhaRtGo-19TQntkpA/H1qZ8yCZu#LCD-I2C%E6%93%8D%E4%BD%9C||
|               mjpg-streamer                  |https://github.com/jacksonliam/mjpg-streamer||
|                  Github download API                |https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28||
|        OpenWrt mounts the SD card to /overlay             |https://blog.csdn.net/u012265809/article/details/121127979||
|    OpenWRT for beginners - Full basic configuration video tutorial |https://www.youtube.com/watch?v=7cxiYmn3OTU&t=2427s||
|        bad CPU type in executable    |https://forum.arduino.cc/t/bad-cpu-type-in-executable-compile-error/1064440/19||
|      Top topics - OpenWrt Forum       |https://forum.openwrt.org/top?period=weekly||
|    Tutorial on installing Mosquitto lightweight MQTT Broker on Raspberry Pi      |https://blog.gtwang.org/iot/raspberry-pi/raspberry-pi-mosquitto-mqtt-broker-iot-integration/2/||
|    Webpage redirect to the main page with CGI Python     |https://stackoverflow.com/questions/6122957/webpage-redirect-to-the-main-page-with-cgi-python|How to write redirect in CGI|

