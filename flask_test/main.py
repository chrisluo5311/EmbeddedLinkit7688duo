from flask import Flask, request, render_template,redirect
import RPi.GPIO as GPIO
import time
app = Flask(__name__)

# define ledPin
ledPin = 14
testOutPin = 15 # input 7688

def setup():
    GPIO.setmode(GPIO.BCM)       
    GPIO.setup(ledPin, GPIO.OUT)   
    GPIO.output(ledPin, GPIO.LOW)  
    
    GPIO.setup(testOutPin, GPIO.OUT,pull_up_down=GPIO.PUD_UP)   
    GPIO.output(testOutPin, GPIO.LOW)  

        
def sound():
    GPIO.setmode(GPIO.BCM)       
    GPIO.setup(ledPin, GPIO.OUT)
    GPIO.setup(testOutPin, GPIO.OUT)
    GPIO.output(ledPin, GPIO.HIGH)  # make ledPin output HIGH level to turn on led   
    GPIO.output(testOutPin, GPIO.HIGH)   # set the ledPin to OUTPUT mode     
    print ('led turned on >>>')     # print information on terminal

def destroy():
    GPIO.setmode(GPIO.BCM)  
    GPIO.setup(ledPin, GPIO.OUT) 
    GPIO.setup(testOutPin, GPIO.OUT)
    GPIO.output(ledPin, GPIO.LOW)
    GPIO.output(testOutPin, GPIO.OUT)   # set the ledPin to OUTPUT mode
    GPIO.cleanup()

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/test")
def test():
    return render_template("flaskform.html")

@app.route("/blink",methods=["GET","POST"])
def blink():
    #setup()
    islight = request.form.get("LED")
    if islight == "U":
        sound()
    else:
        destroy()
    return render_template("flaskform.html")
  


app.run()
