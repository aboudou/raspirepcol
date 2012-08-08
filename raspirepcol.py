#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import random
import array

## Function definitions

# Flash all LED a given number of times
def flashAllLed(number) :
    count = 1
    while count <= number:
        GPIO.output(7, GPIO.HIGH)
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(12, GPIO.HIGH)
        GPIO.output(13, GPIO.HIGH)
        time.sleep(0.25)
        GPIO.output(7, GPIO.LOW)
        GPIO.output(11, GPIO.LOW)
        GPIO.output(12, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        time.sleep(0.25)

        count = count + 1

# Add a new color to light-on and switch to press to the given lists
def addNewColor(gpioPinLedList, gpioPinSwitchList):
    ledNumber = random.randint(1,4)
    gpioPinLed = 0;
    gpioPinSwitch = 0;
    if ledNumber == 1:
        gpioPinLed = 7
        gpioPinSwitch = 15
    elif ledNumber == 2:
        gpioPinLed = 11
        gpioPinSwitch = 16
    elif ledNumber == 3:
        gpioPinLed = 12
        gpioPinSwitch = 18
    elif ledNumber == 4:
        gpioPinLed = 13
        gpioPinSwitch = 22

    gpioPinLedList.append(gpioPinLed)
    gpioPinSwitchList.append(gpioPinSwitch)

## Main section

# Use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)

# Init output pins
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

# Init input pins
GPIO.setup(15, GPIO.IN)
GPIO.setup(16, GPIO.IN)
GPIO.setup(18, GPIO.IN)
GPIO.setup(22, GPIO.IN)

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
