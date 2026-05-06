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
POINTS_COUNT = 400  
original_points = create_fibonacci_sphere(POINTS_COUNT)

# --- 3. 初始化控制與平滑參數 ---
angle_x, angle_y = 0, 0
smoothed_angle_x, smoothed_angle_y = 0, 0
scale = 150
smoothed_scale = 150
alpha = 0.15  # 平滑係數，越小越絲滑

last_hand_pos = None
cap = cv2.VideoCapture(0)

print("正在啟動程式... 按下 'q' 或 'Esc' 鍵可退出視窗。")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # 影像前處理：水平翻轉（像鏡子一樣）
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # 進行手勢辨識
    results = hands.process(rgb_frame)

    # 建立一個全黑畫布用來單獨畫球體
    canvas = np.zeros((h, w, 3), dtype=np.uint8)

    if results.multi_hand_landmarks:
        landmarks = results.multi_hand_landmarks[0]
        
        # A. 計算旋轉 (追蹤手腕 Landmark 0)
        current_pos = np.array([landmarks.landmark[0].x, landmarks.landmark[0].y])
        if last_hand_pos is not None:
            delta = current_pos - last_hand_pos
            angle_y += delta[0] * 5  # 左右移動
            angle_x -= delta[1] * 5  # 上下移動
        last_hand_pos = current_pos

        # B. 計算縮放 (大拇指 4 與 食指 8 的距離)
        thumb = landmarks.landmark[4]
        index = landmarks.landmark[8]
        dist = np.sqrt((thumb.x - index.x)**2 + (thumb.y - index.y)**2)
        scale = 100 + dist * 500

        # C. 套用平滑公式 (防手抖核心)
        smoothed_angle_x = (alpha * angle_x) + (1 - alpha) * smoothed_angle_x
        smoothed_angle_y = (alpha * angle_y) + (1 - alpha) * smoothed_angle_y
        smoothed_scale = (alpha * scale) + (1 - alpha) * smoothed_scale
    else:
        # 手離開畫面時重設追蹤，防止下次手進來時球體瞬間跳轉
        last_hand_pos = None

    # --- 4. 渲染球體 ---
    rotated = rotate_points(original_points, smoothed_angle_x, smoothed_angle_y)
    
    for pt in rotated:
        # 3D 投影到 2D
        u = int(pt[0] * smoothed_scale + w // 2)
        v = int(pt[1] * smoothed_scale + h // 2)
        
        # 根據 z 軸深度決定亮度 (pt[2] 範圍是 -1 到 1)
        brightness = int((pt[2] + 1) * 127) 
        color = (brightness, brightness, 255) # 藍色系粒子
        
        # 檢查座標是否在畫面內才畫
        if 0 <= u < w and 0 <= v < h:
            cv2.circle(canvas, (u, v), 2, color, -1)

    # --- 5. 結合畫面與顯示 (分支功能：同時看手與球) ---
    # 使用透明疊加：60% 原始畫面 + 100% 球體畫布
    debug_view = cv2.addWeighted(frame, 0.6, canvas, 1.0, 0)

    # 在疊加畫面上畫出手部關節線條
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(debug_view, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # 顯示視窗
    cv2.imshow('3D Gesture Sphere - Master View', debug_view)

    # --- 6. 退出機制 ---
    key = cv2.waitKey(5) & 0xFF
    if key == ord('q') or key == ord('Q') or key == 27: # 27 是 Esc
        print("使用者要求退出...")
        break


# 釋放資源
cap.release()
cv2.destroyAllWindows()
