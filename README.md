<h1 style="display: inline;">3D Point Cloud</h1> <h4 style="display: inline;"> &nbsp;&nbsp;&nbsp;&nbsp; 一個透過手勢控制 3D 粒子球體互動系統</h4>
<br>
<br>

![Version](https://img.shields.io/badge/version-v1.0.0-blue?style=flat-square)
![Mediapipe](https://img.shields.io/badge/Mediapipe-0.10.13-green?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.12-yellow?style=flat-square)

## ✨ 特色功能

* **斐波那契球體演算法 (Fibonacci Sphere)**：生成多達 1300 個均勻分佈的粒子，構建極具科技感的數位球體。
* **中指指向控制 (Pointing Control)**：精確計算掌心與中指尖的角度偏移，實現直覺的指向性旋轉。
* **動態縮放 (Pinch Zoom)**：追蹤大拇指與食指距離，即時控制球體大小。
* **指數平滑濾波 (Exponential Smoothing)**：內建防手抖邏輯，讓球體轉動如絲般順滑。
* **全息模式 (Debug Overlay)**：支援攝影機畫面與 3D 粒子畫面的透明疊加顯示，可同時觀察手勢與球體。

---

## 🛠️ 測試環境

* **硬體平台**: Windows( ASUS X515 )
* **Python 版本**: 3.12
* **核心套件**:
    * `mediapipe` (建議 0.10.13)
    * `opencv-python`
    * `numpy`



## 🚀 快速開始

### 1. 複製專案
```bash
git clone [https://github.com/winter-ouo/3D_Point_Cloud.git](https://github.com/winter-ouo/3D_Point_Cloud.git)
cd 3D_Point_Cloud
```

### 2. 建立並啟動虛擬環境
```bash
py -3.12 -m venv .venv
.venv\Scripts\activate
```

### 3. 安裝依賴套件
```bash
pip install mediapipe==0.10.13 opencv-python numpy
```

### 4. 執行程式
```bash
python main.py
```

---

## 🎮 操作說明
* **啟用**：伸出左手，並置於鏡頭畫面中
* **旋轉**：伸出中指，以掌心為基準移動，球體會指向你的中指方向。
* **縮放**：使用大拇指與食指透過「捏合」及「張開」控制球體縮放。
* **退出**：在鏡頭畫面的視窗中，按下 **`q`** 或 **`Esc`** 鍵。

---

## 📂 專案結構

```text
3D_POINT_CLOUD/
├── .venv/               # Python 虛擬環境
├── main.py              # 進入點：整合影像處理與主迴圈
├── geometry.py          # 數學邏輯：存放球體演算法與矩陣運算
├── README.md            # 本說明文件
└── requirements.txt     # 詳細套件清單(含版本)
```

---

## 🧠 技術細節

### 旋轉邏輯 (Rotation Matrix)
我們使用了標準的 X 與 Y 軸旋轉矩陣。點雲 $P$ 經過旋轉矩陣 $R$ 運算得到新座標 $P'$：

$$P' = P \cdot R_x^T \cdot R_y^T$$

### 防手抖公式 (Smoothing)
為了消除指尖微顫，我們對角度與縮放使用了指數平滑公式：

$$Value_{smooth} = (\alpha \cdot Value_{new}) + (1 - \alpha) \cdot Value_{old}$$


---

### 💡 部分參數
* **效能調優**：若在低配環境運行，可修改 `main.py` 中的 `POINTS_COUNT` 至 400-600。
* **初始大小**：可調整 `target_scale = 50 + dist * 400` 中的常數項來改變初始體積。
