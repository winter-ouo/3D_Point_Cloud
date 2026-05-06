import cv2
import mediapipe as mp

# 初始化 MediaPipe 手部偵測模型
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,         # 先偵測一隻手就好，比較省效能
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# 開啟鏡頭 (0 通常是筆電內建鏡頭)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("無法取得鏡頭影像")
        break

    # 為了效能與辨識，將影像轉為 RGB 並水平翻轉（像照鏡子一樣）
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    
    # 進行偵測
    results = hands.process(image)

    # 轉回 BGR 格式以便 OpenCV 顯示
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # 如果有偵測到手，把關節點畫出來
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # 這裡可以拿到特定關節點的座標，例如食指尖 (Landmark 8)
            index_finger_tip = hand_landmarks.landmark[8]
            print(f"食指尖座標: x={index_finger_tip.x:.2f}, y={index_finger_tip.y:.2f}")

    # 顯示視窗
    cv2.imshow('Hand Tracking Test', image)

    # 按下 'q' 鍵退出
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()