#Import the necessary Packages for this software to run
import numpy as np
import cv2
import mediapipe as mp

drawingModule = mp.solutions.drawing_utils
handsModule = mp.solutions.hands

#image mode, confidence values in regards to overall detection and tracking and we will only let two hands be tracked at the same time
#More hands can be tracked at the same time if desired but will slow down the system
mod=handsModule.Hands(min_detection_confidence=0.75, min_tracking_confidence=0.75, max_num_hands=1)

value = 'not detected'
h=480
w=640

#to find postion of the fingers
def findpostion(frame1):
    list=[]
    results = mod.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks != None:
       for handLandmarks in results.multi_hand_landmarks:
           drawingModule.draw_landmarks(frame1, handLandmarks, handsModule.HAND_CONNECTIONS,drawingModule.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=4),drawingModule.DrawingSpec(color=(180, 255, 255), thickness=2, circle_radius=2),)
           list=[]
           for id, pt in enumerate (handLandmarks.landmark):
                x = int(pt.x * w)
                y = int(pt.y * h)
                list.append([id,x,y])

    return list            

#to find name of landmakrs in the fingers
def findnameoflandmark(frame1):
     list=[]
     results = mod.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
     if results.multi_hand_landmarks != None:
        for handLandmarks in results.multi_hand_landmarks:
            for point in handsModule.HandLandmark:
                 list.append(str(point).replace ("< ","").replace("HandLandmark.", "").replace("_"," ").replace("[]",""))
     return list
#this is a getter to find left or right hand 
def getLeftOrRight():
    return value
#this recognize the hand and add a rectangle to the hand
def rectangle(debug_image,hand_sign_text):
     global value
     results = mod.process(cv2.cvtColor(debug_image, cv2.COLOR_BGR2RGB))
     
     if results.multi_hand_landmarks != None:
        for hand_landmarks in results.multi_hand_landmarks:
            
           handIndex = results.multi_hand_landmarks.index(hand_landmarks)
           handLabel = results.multi_handedness[handIndex].classification[0].label
           handLandmarks = []
           
           for landmarks in hand_landmarks.landmark:
               handLandmarks.append([landmarks.x, landmarks.y])
               
           if handLabel == "Left":
               value = "right"
           else:
               value = "left"
               
           brect = calc_bounding_rect(debug_image, hand_landmarks)
           debug_image = draw_info_text(debug_image,
                    brect,
                    value,
                    hand_sign_text
                    )
     return debug_image 

#calculate the position of the hand to add that recatangle
def calc_bounding_rect(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_array = np.empty((0, 2), int)

    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point = [np.array((landmark_x, landmark_y))]

        landmark_array = np.append(landmark_array, landmark_point, axis=0)

    x, y, w, h = cv2.boundingRect(landmark_array)

    return [x, y, x + w, y + h]

#showing info on that recatangle
def draw_info_text(image, brect,LeftOrRight,hand_sign_text):
    # Outer rectangle
    cv2.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]),
                     (0, 0, 0), 1)
    # info rectangle
    cv2.rectangle(image, (brect[0], brect[1]), (brect[2], brect[1] - 22),
                 (0, 0, 0), -1)

    info_text = LeftOrRight
    if hand_sign_text != '':
         info_text = info_text + ':' + hand_sign_text
    cv2.putText(image, info_text, (brect[0] + 5, brect[1] - 4),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

    return image

