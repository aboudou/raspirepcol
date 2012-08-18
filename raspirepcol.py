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

# Flash all LED three times : the game is about to start
flashAllLed(3)

# Select difficulty
basetime = 1.0
print ("Choose difficulty by pressing one of the four buttons.")
print ("Then validate by pressing again the same button or choose another "
+ "difficulty by pressing another button.")
difficulty = 0
firstChoice = -1
while difficulty == 0:
    # Wait for the user to press a button
    while firstChoice == -1:
        position = 0
        while position < len(gpioPinSwitchListAvail):
            if GPIO.input(gpioPinSwitchListAvail[position]) == GPIO.LOW:
                firstChoice = position
            position += 1

    # Light-up the related LEDs
    position = 0
    while position < len(gpioPinLedListAvail):
        if position <= firstChoice:
            GPIO.output(gpioPinLedListAvail[position], GPIO.HIGH)
        else:
            GPIO.output(gpioPinLedListAvail[position], GPIO.LOW)
        position += 1

    # Wait for the user to release switch
    while GPIO.input(gpioPinSwitchListAvail[firstChoice]) == GPIO.LOW:
        time.sleep(0.25)

    # Wait for the user to confirm difficulty
    secondChoice = -1
    while secondChoice == -1:
        position = 0
        while position < len(gpioPinSwitchListAvail):
            if GPIO.input(gpioPinSwitchListAvail[position]) == GPIO.LOW:
                secondChoice = position
            position += 1

    # Check if the difficulty was confirmed
    if secondChoice == firstChoice:
        difficulty = secondChoice + 1
        flashAllLed(2)
        time.sleep(2)
    else:
        firstChoice = secondChoice
        
basetime = basetime / difficulty 

print("")
print("Choosen difficulty : " + str(difficulty) + "/4")
print("")
print("Hit Ctrl + C to stop the game")

while True:
    # Add a new random color to array (and the corresponding switch)
    addNewColor(gpioPinLedList, gpioPinSwitchList)

    # Play colors in array
    for gpioPinLed in gpioPinLedList:
        GPIO.output(gpioPinLed, GPIO.HIGH)
        time.sleep(basetime)
        GPIO.output(gpioPinLed, GPIO.LOW)
        time.sleep(basetime / 2)

    # Wait for user input
    error = False
    position = 0
    while error == False and position < len(gpioPinSwitchList):
        switchPressed = False
        switchNumber = 0
        while switchPressed == False:
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
