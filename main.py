import cv2
import numpy as np
import mediapipe as mp
from geometry import create_fibonacci_sphere, rotate_points

# --- 1. 初始化 MediaPipe ---
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.8
)

# --- 2. 準備球體原始資料 ---
POINTS_COUNT = 2000
original_points = create_fibonacci_sphere(POINTS_COUNT)

# --- 3. 初始化控制與平滑參數 ---
smoothed_angle_x, smoothed_angle_y = 0, 0
smoothed_scale = 150
alpha = 0.15  # 平滑係數

cap = cv2.VideoCapture(0)

print("正在啟動『指向控制』模式... 按下 'q' 或 'Esc' 鍵可退出。")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # 建立全黑畫布
    canvas = np.zeros((h, w, 3), dtype=np.uint8)

    if results.multi_hand_landmarks:
        landmarks = results.multi_hand_landmarks[0]
        
        # --- 新的旋轉邏輯：中指(12)相對於掌心(9)的指向 ---
        palm = landmarks.landmark[9]
        middle_tip = landmarks.landmark[12]

        # 計算向量位移
        dx = middle_tip.x - palm.x
        dy = middle_tip.y - palm.y
        
        # 使用 arctan2 算出相對角度，並乘以係數來放大旋轉感
        # 這會讓你的手指微動，球體就有明顯的轉向
        target_angle_y = np.arctan2(dx, 0.2) * 2.5
        target_angle_x = -np.arctan2(dy, 0.2) * 2.5

        # 縮放邏輯：大拇指(4)與食指(8)的距離
        thumb = landmarks.landmark[4]
        index = landmarks.landmark[8]
        dist = np.sqrt((thumb.x - index.x)**2 + (thumb.y - index.y)**2)
        target_scale = 50 + dist * 400

        # --- 套用平滑化 (避免指尖微顫) ---
        smoothed_angle_x = (alpha * target_angle_x) + (1 - alpha) * smoothed_angle_x
        smoothed_angle_y = (alpha * target_angle_y) + (1 - alpha) * smoothed_angle_y
        smoothed_scale = (alpha * target_scale) + (1 - alpha) * smoothed_scale
    else:
        # 手離開時，維持在最後的角度或慢慢歸零 (這裡選擇維持)
        pass

    # --- 4. 渲染球體 ---
    rotated = rotate_points(original_points, smoothed_angle_x, smoothed_angle_y)
    
    for pt in rotated:
        # 3D 投影到 2D
        u = int(pt[0] * smoothed_scale + w // 2)
        v = int(pt[1] * smoothed_scale + h // 2)
        
        # 根據 Z 深度調整亮度
        brightness = int((pt[2] + 1) * 127) 
        color = (brightness, brightness, 255) 
        
        if 0 <= u < w and 0 <= v < h:
            cv2.circle(canvas, (u, v), 2, color, -1)

    # --- 5. 結合畫面與顯示 ---
    debug_view = cv2.addWeighted(frame, 0.5, canvas, 1.0, 0)

    # 在畫面上標示出我們正在參考的兩個點 (掌心與中指尖)
    if results.multi_hand_landmarks:
        # 畫出所有關節
        mp_drawing.draw_landmarks(debug_view, landmarks, mp_hands.HAND_CONNECTIONS)
        
        # 額外圈出參考點，讓你知道現在在對準哪裡
        p_x, p_y = int(palm.x * w), int(palm.y * h)
        m_x, m_y = int(middle_tip.x * w), int(middle_tip.y * h)
        cv2.circle(debug_view, (p_x, p_y), 8, (0, 255, 0), 2)  # 綠色圈掌心
        cv2.circle(debug_view, (m_x, m_y), 8, (0, 255, 255), 2) # 黃色圈中指尖

    cv2.imshow('3D Sphere - Pointing Control Mode', debug_view)

    # --- 6. 退出機制 ---
    key = cv2.waitKey(5) & 0xFF
    if key == ord('q') or key == ord('Q') or key == 27:
        print("使用者要求退出...")
        break

cap.release()
cv2.destroyAllWindows()