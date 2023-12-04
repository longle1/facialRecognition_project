# Include the library files
import face_recognition
import cv2
import time
import os
import pickle
import I2C_LCD_driver
import RPi.GPIO as GPIO
from time import sleep
import requests


encodings = []
names = []


def check_password(username, password):
    try:
        url = "http://api-server-nt131.onrender.com/api/v1/users/check-password"  # Thay thế bằng URL thực tế
        data = {
            "username": username,
            "password": password
        }
        response = requests.post(url, json=data)
        response.raise_for_status()
        
        # Xử lý phản hồi từ API
        result = response.json()
        if result["status"]:
            return True
        else:
            return False
    
    except requests.exceptions.RequestException as e:
        return False


def face_recognition(username):
    try:
        url = "http://api-server-nt131.onrender.com/api/v1/users/face-recognition"  # Thay thế bằng URL thực tế
        data = {
            "username": username
        }
        response = requests.post(url, json=data)
        response.raise_for_status()
        
        # Xử lý phản hồi từ API
        result = response.json()
        if result["status"]:
            return True
        else:
            return False

    except requests.exceptions.RequestException as e:
        return False

# load all encoding files after train
with open('train.pkl', 'rb') as f:
    names = pickle.load(f)
    encodings = pickle.load(f)


#when user presses letter 'A', the camera is opened and conduct to recognizer
def facial_recognizer():
    cam = cv2.VideoCapture(1)
    start_time = time.time()  
    while True:
        _, frame = cam.read()
        frameSize = cv2.resize(frame, (0, 0), fx=.33, fy=.33)
        frame = cv2.cvtColor(frameSize, cv2.COLOR_RGB2BGR)
        face_locations = face_recognition.face_locations(frame, model='cnn')
        allEncodings = face_recognition.face_encodings(frame, face_locations)
        for (top, right, bottom, left), face_encoding in zip(face_locations,  allEncodings):
            name="unKnown"
            matches = face_recognition.compare_faces(encodings, face_encoding)
            if True in matches:
                first_match_index = matches.index(True)
                name=name_faces[first_match_index]
                checkSuccessful()
                face_recognition("user")
                cam.release()
                cv2.destroyAllWindows()
                return

        
        current_time = time.time()  
        elapsed_time = current_time - start_time  
        if elapsed_time >= 10:  
            break

    cam.release()
    cv2.destroyAllWindows()
    

def checkSuccessful():
    if relayState:
        GPIO.output(Relay,GPIO.LOW)
        sleep(5) 
        relayState = False
        
    elif relayState == False:   # if state is blocking, transfering state to open 
        GPIO.output(Relay,GPIO.HIGH)
        sleep(5)
        relayState = True


# Enter column pins
C1 = 5
C2 = 6
C3 = 13
C4 = 19

# Enter row pins
R1 = 12
R2 = 16
R3 = 20
R4 = 21


# Enter LED pin
Relay = 27
relayState = True   #true is blocked

# Create a object for the LCD
lcd = I2C_LCD_driver.lcd()

#Starting text
lcd.lcd_display_string("System loading",1,1)
for a in range (0,16):
    lcd.lcd_display_string(".",2,a)
    sleep(0.1)

lcd.lcd_clear()

# The GPIO pin of the column of the key that is currently
# being held down or -1 if no key is pressed
keypadPressed = -1


input = ""

# Setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # helps refer to GPIO pins in numerical order
GPIO.setup(Relay,GPIO.OUT)
GPIO.output(Relay,GPIO.HIGH)


# Set column pins as output pins
GPIO.setup(C1, GPIO.OUT)
GPIO.setup(C2, GPIO.OUT)
GPIO.setup(C3, GPIO.OUT)
GPIO.setup(C4, GPIO.OUT)

# Set row pins as input pins
GPIO.setup(R1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(R2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(R3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(R4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# This callback registers the key that was pressed
# if no other key is currently pressed
def keypadCallback(channel):
    global keypadPressed
    if keypadPressed == -1:
        keypadPressed = channel

# Detect the rising edges
GPIO.add_event_detect(R1, GPIO.RISING, callback=keypadCallback) # Rising means following event when increasing from low edge to high edge on GPIO pin
GPIO.add_event_detect(R2, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(R3, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(R4, GPIO.RISING, callback=keypadCallback)

# Sets all rows to a specific state. 
def setAllRows(state):
    GPIO.output(C1, state)
    GPIO.output(C2, state)
    GPIO.output(C3, state)
    GPIO.output(C4, state)

# Check or clear PIN
def commands():
    global relayState
    global input
    pressed = False

    GPIO.output(C1, GPIO.HIGH)
    

    # Clear PIN 
    if (GPIO.input(R1) == 1):
        print("Input reset!");
        lcd.lcd_clear()
        lcd.lcd_display_string("Clear",1,5)
        sleep(1)
        pressed = True

    GPIO.output(C1, GPIO.HIGH)

    # Check PIN
    if (not pressed and GPIO.input(R2) == 1):
        if check_password("user", input):
            checkSuccessful()
            
        else:
            checkError()
        pressed = True

    GPIO.output(C1, GPIO.LOW)

    GPIO.output(C1, GPIO.HIGH)

    if(not pressed and GPIO.input(R4) == 1):
        facial_recognizer() #call recognition face
        pressed = True

    GPIO.output(C1, GPIO.LOW)

    if pressed:
        input = ""

    return pressed

# reads the columns and appends the value, that corresponds
# to the button, to a variable
def read(column, characters):
    global input

    GPIO.output(column, GPIO.HIGH)
    if(GPIO.input(R1) == 1):
        input = input + characters[0]
        print(input)
        lcd.lcd_display_string(str(input),2,0)
    if(GPIO.input(R2) == 1):
        input = input + characters[1]
        print(input)
        lcd.lcd_display_string(str(input),2,0)
    if(GPIO.input(R3) == 1):
        input = input + characters[2]
        print(input)
        lcd.lcd_display_string(str(input),2,0)
    if(GPIO.input(R4) == 1):
        input = input + characters[3]
        print(input)
        lcd.lcd_display_string(str(input),2,0)
    GPIO.output(column, GPIO.LOW)

try:
    while True:       
        lcd.lcd_display_string("Enter your PIN:",1,0)
        
        # If a button was previously pressed,
        # check, whether the user has released it yet
        if keypadPressed != -1:
            setAllRows(GPIO.HIGH)
            if GPIO.input(keypadPressed) == 0:
                keypadPressed = -1
            else:
                sleep(0.1)
        # Otherwise, just read the input
        else:
            if not commands():
                read(C1, ["D","C","B","A"])
                read(C2, ["#","9","6","3"])
                read(C3, ["0","8","5","2"])
                read(C4, ["*","7","4","1"])
                sleep(0.1)
            else:
                sleep(0.1)
except KeyboardInterrupt:
    print("Stopped!")


