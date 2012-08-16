#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import random
import array
import signal

## Function definitions

# Init all pins
def initPins():
    # Init output pins
    for gpioPin in gpioPinLedListAvail:
        GPIO.setup(gpioPin, GPIO.OUT)

    # Init input pins
    for gpioPin in gpioPinSwitchListAvail:
        GPIO.setup(gpioPin, GPIO.IN)

# Flash all LED a given number of times
def flashAllLed(number) :
    count = 1
    while count <= number:
        for gpioPin in gpioPinLedListAvail:
            GPIO.output(gpioPin, GPIO.HIGH)
        
        time.sleep(0.25)

        for gpioPin in gpioPinLedListAvail:
            GPIO.output(gpioPin, GPIO.LOW)
        
        time.sleep(0.25)

        count = count + 1

# Add a new color to light-on and switch to press to the given lists
def addNewColor(gpioPinLedList, gpioPinSwitchList):
    number = random.randint(0,3)
    
    gpioPinLedList.append(gpioPinLedListAvail[number])
    gpioPinSwitchList.append(gpioPinSwitchListAvail[number])


# Called on process interruption. Set all pins to "Input" default mode.
def endProcess(signalnum = None, handler = None):
    for gpioPinLed in gpioPinLedListAvail:
        GPIO.setup(gpioPinLed, GPIO.IN)
    exit(0)


## Main section

# Prepare handlers for process exit
signal.signal(signal.SIGTERM, endProcess)
signal.signal(signal.SIGINT, endProcess)

# Init list of available LED and switches pins
gpioPinLedListAvail = [7, 11, 12, 13]
gpioPinSwitchListAvail = [15, 16, 18, 22]

# Use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)

# Init pins
initPins()

# Init empty lists of colors and switches
gpioPinLedList = []
gpioPinSwitchList = []

# Flash all LED three times : the game is close to start
flashAllLed(3)
time.sleep(2)

while True:
    # Add a new random color to array (and the corresponding switch)
    addNewColor(gpioPinLedList, gpioPinSwitchList)

    # Play colors in array
    for gpioPinLed in gpioPinLedList:
        GPIO.output(gpioPinLed, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(gpioPinLed, GPIO.LOW)
        time.sleep(0.5)

    # Wait for user input
    error = False
    position = 0
    while error == False and position < len(gpioPinSwitchList):
        switchPressed = False
        switchNumber = 0
        while switchPressed == False:
           """
           if GPIO.input(15) == GPIO.LOW:
               switchNumber = 15
               switchPressed = True
           if GPIO.input(16) == GPIO.LOW:
               switchNumber = 16
               switchPressed = True
           if GPIO.input(18) == GPIO.LOW:
               switchNumber = 18
               switchPressed = True
           if GPIO.input(22) == GPIO.LOW:
               switchNumber = 22
               switchPressed = True
           """
           for gpioPin in gpioPinSwitchListAvail:
               if GPIO.input(gpioPin) == GPIO.LOW:
                   switchNumber = gpioPin
                   switchPressed = True

           # Check for validity
           if switchPressed == True:
               if switchNumber != gpioPinSwitchList[position]:
                   # If KO, flash all LED three times, empty colors and switches
                   # lists and start again
                   flashAllLed(3)
                   time.sleep(1)

                   error = True

                   gpioPinSwitchList = []
                   gpioPinLedList = []
               
               else:
                   # Flash LED once
                   GPIO.output(gpioPinLedList[position], GPIO.HIGH)
                   time.sleep(0.5)
                   GPIO.output(gpioPinLedList[position], GPIO.LOW)

        position = position+1

    time.sleep(1)
