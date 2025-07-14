# On-Screen Writing with Index Finger using OpenCV and Mediapipe (with color selection)

import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

canvas = None
drawing = False
prev_x, prev_y = None, None

# Define available colors (BGR)
colors = [(0, 255, 255), (255, 0, 255), (255, 255, 0), (0, 255, 0), (0, 0, 255), (255, 0, 0)]
color_names = ["Yellow", "Pink", "Cyan", "Green", "Red", "Blue"]
color_idx = 0

def fingers_up(hand_landmarks):
    tips = [
        mp_hands.HandLandmark.THUMB_TIP,
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]
    pips = [
        mp_hands.HandLandmark.THUMB_IP,
        mp_hands.HandLandmark.INDEX_FINGER_PIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
        mp_hands.HandLandmark.RING_FINGER_PIP,
        mp_hands.HandLandmark.PINKY_PIP
    ]
    fingers = []
    for tip, pip in zip(tips, pips):
        if tip == mp_hands.HandLandmark.THUMB_TIP:
            fingers.append(hand_landmarks.landmark[tip].x < hand_landmarks.landmark[pip].x)
        else:
            fingers.append(hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y)
    return fingers  # [thumb, index, middle, ring, pinky]

# ...existing code...

with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) as hands:

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        if canvas is None:
            canvas = np.zeros_like(frame)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        # --- Color palette right alignment ---
        palette_width = len(colors) * 60
        img_w = frame.shape[1]
        for i, col in enumerate(colors):
            x1 = img_w - palette_width + i*60
            y1 = 10
            x2 = x1 + 40
            y2 = y1 + 40
            cv2.rectangle(frame, (x1, y1), (x2, y2), col, -1)
            if i == color_idx:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255,255,255), 3)
            cv2.putText(frame, color_names[i], (x1, y2+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, col, 2)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                fingers = fingers_up(hand_landmarks)
                ix = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * frame.shape[1])
                iy = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * frame.shape[0])

                # Color selection: if index finger is up and tip is over a color button
                if fingers == [False, True, False, False, False]:
                    cv2.circle(frame, (ix, iy), 8, (255, 0, 255), -1)
                    for i in range(len(colors)):
                        x1 = img_w - palette_width + i*60
                        y1 = 10
                        x2 = x1 + 40
                        y2 = y1 + 40
                        if x1 < ix < x2 and y1 < iy < y2:
                            color_idx = i
                    # Draw on canvas
                    if iy > 60:  # Prevent drawing when selecting color
                        if prev_x is not None and prev_y is not None:
                            cv2.line(canvas, (prev_x, prev_y), (ix, iy), colors[color_idx], 6)
                        prev_x, prev_y = ix, iy
                    else:
                        prev_x, prev_y = None, None
                else:
                    prev_x, prev_y = None, None

        # Overlay the canvas on the frame
        frame = cv2.addWeighted(frame, 0.7, canvas, 0.7, 0)

        # --- Caption left alignment ---
        cv2.putText(frame, "Draw with your index finger (raise only index)", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
        cv2.putText(frame, "Press 'c' to clear, ESC to exit", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
        cv2.putText(frame, "Touch color box to change color", (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 2)

        # --- Full screen window ---
        cv2.namedWindow("On-Screen Writing", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("On-Screen Writing", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        cv2.imshow("On-Screen Writing", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break
        elif key == ord('c'):
            canvas = np.zeros_like(frame)

cap.release()
cv2.destroyAllWindows()