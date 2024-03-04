# Hand Gestures untuk kontrol volume beserta notifikasi

import cv2
import pyautogui
import mediapipe as mp
import pygame

pygame.mixer.init()
volume_up_sound = pygame.mixer.Sound("naik.mp3")
volume_down_sound = pygame.mixer.Sound("turun.mp3")

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)

mp_drawing = mp.solutions.drawing_utils

volume_text_position = (10, 460)

def change_system_volume(direction):
    pyautogui.press('volumedown' if direction == 'down' else 'volumeup')

    if direction == 'up':
        volume_up_sound.play()
    elif direction == 'down':
        volume_down_sound.play()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

            if index_finger_y < thumb_y:
                change_system_volume('up')
            elif index_finger_y > thumb_y:
                change_system_volume('down')

    cv2.imshow('Hand Gesture', frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()