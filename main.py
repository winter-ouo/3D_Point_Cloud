import cv2
import numpy as np
import mediapipe as mp
from geometry import create_fibonacci_sphere, rotate_points

# 初始化 MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7, # 提高門檻，不確定的點就不抓
    min_tracking_confidence=0.8   # 提高追蹤穩定度，這對防手抖很有幫助
)

# 準備球體原始資料
POINTS_COUNT = 400  # 粒子數量，ASUS X515 建議 400-600
original_points = create_fibonacci_sphere(POINTS_COUNT)

# 初始化球體參數
angle_x, angle_y = 0, 0
scale = 150
last_hand_pos = None

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # 建立一個全黑的畫布來放球體
    canvas = np.zeros((h, w, 3), dtype=np.uint8)

    if results.multi_hand_landmarks:
        landmarks = results.multi_hand_landmarks[0]
        
        # 1. 旋轉邏輯：追蹤手腕 (Landmark 0) 的移動
        current_pos = np.array([landmarks.landmark[0].x, landmarks.landmark[0].y])
        if last_hand_pos is not None:
            delta = current_pos - last_hand_pos
            angle_y += delta[0] * 5  # 左右移動繞 Y 軸轉
            angle_x -= delta[1] * 5  # 上下移動繞 X 軸轉
        last_hand_pos = current_pos

        # 2. 縮放邏輯：大拇指(4)與食指(8)的距離
        t = landmarks.landmark[4]
        i = landmarks.landmark[8]
        dist = np.sqrt((t.x - i.x)**2 + (t.y - i.y)**2)
        scale = 100 + dist * 500  # 將距離映射到縮放倍率

    # 3. 執行旋轉與投影
    rotated = rotate_points(original_points, angle_x, angle_y)
    
    for pt in rotated:
        # 將 3D (x, y, z) 投影到 2D (u, v)
        # z 軸用來決定顏色深淺（立體感）
        u = int(pt[0] * scale + w // 2)
        v = int(pt[1] * scale + h // 2)
        
        # 根據深度 (z) 調整亮度，z 越正越靠近鏡頭（越亮）
        brightness = int((pt[2] + 1) * 127) 
        color = (brightness, brightness, 255) # 淡淡的藍色粒子
        
        # 畫在畫布上
        cv2.circle(canvas, (u, v), 2, color, -1)

    # 結合原始鏡頭畫面（小視窗）與球體畫布
    cv2.imshow('3D Gesture Sphere', canvas)

    # 讀取一次按鍵紀錄，存入 key 變數
    # waitKey(5) 代表等待 5 毫秒，這對 ASUS X515 的效能很平衡
    key = cv2.waitKey(5) & 0xFF
    
    # 同時檢查 'q' (小寫), 'Q' (大寫) 或 'Esc' (27)
    if key == ord('q') or key == ord('Q') or key == 27:
        print("使用者要求退出...")
        break

# 迴圈結束後的善後
cap.release()
cv2.destroyAllWindows()