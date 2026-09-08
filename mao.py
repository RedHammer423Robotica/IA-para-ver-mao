
import cv2

import mediapipe as mp
import serial
import time

# Troque pela sua porta Bluetooth
ser = serial.Serial("COM4", 115200)
time.sleep(2)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    
    

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            tip = handLms.landmark[8]
            base = handLms.landmark[6]


            if tip.y < base.y:
                ser.write(b"GIRAR\n")
                print("OPEN")
            else:
                ser.write(b"PARAR\n")
                print("CLOSE")

    cv2.imshow("Camera", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
