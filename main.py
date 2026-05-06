import cv2
import numpy as np
import mediapipe as mp
from geometry import create_fibonacci_sphere, rotate_points

# 初始化 MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.8
)

POINTS_COUNT = 400
original_points = create_fibonacci_sphere(POINTS_COUNT)

# --- 【新增】平滑參數初始化 ---
angle_x, angle_y = 0, 0
smoothed_angle_x, smoothed_angle_y = 0, 0
scale = 150
smoothed_scale = 150
alpha = 0.15  # 平滑係數：0.1 很滑但有延遲，0.3 較靈敏但微抖
# --------------------------

last_hand_pos = None
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    canvas = np.zeros((h, w, 3), dtype=np.uint8)

    if results.multi_hand_landmarks:
        landmarks = results.multi_hand_landmarks[0]
        
        # 1. 計算旋轉
        current_pos = np.array([landmarks.landmark[0].x, landmarks.landmark[0].y])
        if last_hand_pos is not None:
            delta = current_pos - last_hand_pos
            angle_y += delta[0] * 5
            angle_x -= delta[1] * 5
        last_hand_pos = current_pos

        # 2. 計算縮放
        t = landmarks.landmark[4]
        i = landmarks.landmark[8]
        dist = np.sqrt((t.x - i.x)**2 + (t.y - i.y)**2)
        scale = 100 + dist * 500

        # --- 【核心修改】套用指數平滑公式 ---
        # 過濾掉突發的小跳動，讓球體轉動有「阻尼感」
        smoothed_angle_x = (alpha * angle_x) + (1 - alpha) * smoothed_angle_x
        smoothed_angle_y = (alpha * angle_y) + (1 - alpha) * smoothed_angle_y
        smoothed_scale = (alpha * scale) + (1 - alpha) * smoothed_scale
        # ----------------------------------
    else:
        # 當手離開畫面，重設追蹤位置，避免下次手進來時球體噴飛
        last_hand_pos = None

    # 3. 使用「平滑後」的數據進行繪製
    # 注意：這裡要把原本的 angle 改成 smoothed_angle
    rotated = rotate_points(original_points, smoothed_angle_x, smoothed_angle_y)
    
    for pt in rotated:
        # 使用 smoothed_scale 縮放
        u = int(pt[0] * smoothed_scale + w // 2)
        v = int(pt[1] * smoothed_scale + h // 2)
        
        brightness = int((pt[2] + 1) * 127) 
        color = (brightness, brightness, 255)
        cv2.circle(canvas, (u, v), 2, color, -1)

    cv2.imshow('3D Gesture Sphere', canvas)

    key = cv2.waitKey(5) & 0xFF
    if key == ord('q') or key == ord('Q') or key == 27:
        print("使用者要求退出...")
        break

cap.release()
cv2.destroyAllWindows()