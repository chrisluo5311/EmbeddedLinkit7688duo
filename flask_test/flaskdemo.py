from flask import Flask, request, render_template,redirect
#import RPi.GPIO as GPIO
import time
app = Flask(__name__)

# define ledPin
ledPin = 14

# def setup():
#     GPIO.setmode(GPIO.BOARD)       # use PHYSICAL GPIO Numbering
#     GPIO.setup(ledPin, GPIO.OUT)   # set the ledPin to OUTPUT mode
#     GPIO.output(ledPin, GPIO.LOW)  # make ledPin output LOW level
#     print ('using pin%d'%ledPin)
#
# def loop():
#     while True:
#         GPIO.output(ledPin, GPIO.HIGH)  # make ledPin output HIGH level to turn on led
#         print ('led turned on >>>')     # print information on terminal
#         time.sleep(1)                   # Wait for 1 second
#         GPIO.output(ledPin, GPIO.LOW)   # make ledPin output LOW level to turn off led
#         print ('led turned off <<<')
#         time.sleep(1)                   # Wait for 1 second
#
# def destroy():
#     GPIO.cleanup()
def hellofromdef():
    return "Blink"

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/test")
def test():
    return render_template("flaskform.html")

@app.route("/blink",methods=["GET","POST"])
def blink():
    islight = request.form.get("LED")
    if islight == "U":
        # setup()
        # loop()
        islight = hellofromdef()
    else:
        print("關閉Led燈")
        # destroy()

    return 'Led按的是 => {}'.format(islight)

if __name__ == "__main__":
    app.run()