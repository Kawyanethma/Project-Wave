#Import the necessary Packages for this software to run
import mediapipe as mp
import cv2
import RPi.GPIO as GPIO

from collections import Counter
from module import findnameoflandmark,findpostion,getLeftOrRight,rectangle

#Use MediaPipe to draw the hand framework over the top of hands it identifies in Real-Time
drawingModule = mp.solutions.drawing_utils
handsModule = mp.solutions.hands

#If code is stopped during active it will stay active
#This may produce a warning if restarted, this
#line prevents that.
GPIO.setwarnings(False)
# #This means we will refer to the GPIO
# #by the number after GPIO.
GPIO.setmode(GPIO.BCM)
# #This sets up the GPIO 18 pin as an output pin
GPIO.setup(18, GPIO.OUT)

#Use CV2 Functionality to create a Video stream and add some values
#Add confidence values and extra settings to MediaPipe hand tracking. As we are using a live video stream this is not a static

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
tipIds = [4, 8, 12, 16, 20]
tipname = [4, 8, 12, 16, 20]
fingers=[]

power = 'not assign'
hand_sign_text = ''

#Create an infinite loop which will produce the live feed to our desktop and that will search for hands
while cap.isOpened():
       ret, frame = cap.read()

       #Determines the frame size, 640 x 480 offers a nice balance between speed and accurate identification
       frame1 = cv2.resize(frame, (640, 480))

       a=findpostion(frame1)
       b=findnameoflandmark(frame1)
       frame1 = rectangle(frame1,hand_sign_text)
       check = getLeftOrRight()

       if len(b and a)!=0:
            fingers=[]

            #left hand
            if check == 'left' and a[tipIds[0]][1] < a[tipIds[0] - 1][1]:
                fingers.append(1)
                print (b[4])

            else:
                fingers.append(0)

            #right hand
            if check == 'right' and a[tipIds[0]][1] > a[tipIds[0] - 1][1]:
                fingers.append(1)
                print (b[4])

            else:
                fingers.append(0)


            for id in range(1,5):

                if a[tipIds[id]][2] < a[tipIds[id]-2][2]:
                    print(b[tipname[id]])

                    fingers.append(1)

                else:
                    fingers.append(0)
       #Below will print to the terminal the number of fingers that are up or down
       totalFingers = fingers.count(1)
       up=totalFingers
       down=5-totalFingers

       print('This many fingers are up - ', up)
       print('This many fingers are down - ', down)

       if up == 5:
            power = 'ON'
            hand_sign_text = 'open'
            GPIO.output(18, 1)

       if up == 0:
            power = 'OFF'
            hand_sign_text = 'close'
            GPIO.output(18, 0)

       if up != 0 and up != 5:
           hand_sign_text = ''


       cv2.putText(frame1, 'Switch : '+str(power), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 1, cv2.LINE_AA)
       cv2.putText(frame1, 'Opened fingers: '+str(up), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1, cv2.LINE_AA)
       cv2.imshow("Hand Gesture Recognition", frame1);

       #Below states that if the |esc| is press on the keyboard it will stop the system
       if cv2.waitKey(5) & 0xFF == 27:
          break

cap.release()
cv2.destroyAllWindows()
