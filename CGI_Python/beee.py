from pyfirmata import Arduino

port ='COM8'
board = Arduino(port)

pin = 13
board.digital[pin].write(1)