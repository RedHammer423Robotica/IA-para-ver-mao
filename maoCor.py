import cv2
import mediapipe as mp
import serial
import time
import numpy as np

# Troque pela sua porta Bluetooth
ser = serial.Serial("COM4", 115200)
time.sleep(2)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# ========== CONFIGURAÇÃO DA COR ==========
# Defina aqui a cor HSV que você quer detectar
# Exemplo: azul (luva/pulseira). Ajuste esses valores!
lower_color = np.array([40, 50, 50])   # H mínimo, S mínimo, V mínimo
upper_color = np.array([80, 255, 255]) # H máximo, S máximo, V máximo

# Para descobrir os valores HSV da sua cor, use o script auxiliar no final da mensagem

while True:
    success, img = cap.read()
    if not success:
        continue

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # Pega as coordenadas da mão na imagem (para verificar a cor na região)
            h, w, _ = img.shape
            landmarks = handLms.landmark
            
            # Cria uma máscara da cor desejada
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower_color, upper_color)
            
            # Verifica se há pixels da cor na região da mão
            # Pega o bounding box aproximado da mão
            x_coords = [int(lm.x * w) for lm in landmarks]
            y_coords = [int(lm.y * h) for lm in landmarks]
            
            x_min, x_max = max(0, min(x_coords) - 20), min(w, max(x_coords) + 20)
            y_min, y_max = max(0, min(y_coords) - 20), min(h, max(y_coords) + 20)
            
            roi_mask = mask[y_min:y_max, x_min:x_max]
            color_pixels = cv2.countNonZero(roi_mask)
            
            # Só processa se tiver pixels suficientes da cor na mão
            MIN_PIXELS = 40  # Ajuste conforme necessário
            
            if color_pixels > MIN_PIXELS:
                mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

                # Dedo indicador: ponta (8) vs base (6)
                indicador_levantado = handLms.landmark[8].y < handLms.landmark[6].y
                
                # Dedo do meio: ponta (12) vs base (10)
                meio_levantado = handLms.landmark[12].y < handLms.landmark[10].y

                # Só envia GIRAR se AMBOS estiverem levantados
                if indicador_levantado and meio_levantado:
                    ser.write(b"GIRAR\n")
                    print("INDICADOR + MEIO LEVANTADOS → GIRAR")
                    cv2.putText(img, "GIRAR", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    ser.write(b"PARAR\n")
                    print("PARAR")
                    cv2.putText(img, "PARAR", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                # Mão detectada mas sem a cor → ignora
                cv2.putText(img, "COR NAO DETECTADA", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

    cv2.imshow("Camera", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()