# 3D Point Cloud
### 🖐️ 手勢控制 3D 粒子球體互動系統

這是一個結合電腦視覺與 3D 數學幾何的互動專案。透過筆電鏡頭追蹤手勢，即時操控一個由均勻點陣組成的 3D 粒子球體，實現旋轉、縮放與空間互動。

---

## 🛠 技術規格 (Technical Specs)

| 類別 | 項目 | 說明 |
| :--- | :--- | :--- |
| **硬體平台** | ASUS X515 | 針對內建鏡頭與 CPU 運算優化 |
| **開發環境** | Python 3.x | 建議使用 `venv` 虛擬環境隔離 |
| **手勢辨識** | MediaPipe Hands | Google 提供之高效能手部 21 關節點追蹤 |
| **渲染引擎** | OpenCV | 負責座標投影與 2D 畫布即時渲染 |
| **數學運算** | NumPy | 處理 3D 旋轉矩陣 (Rotation Matrix) 與點雲座標 |

---

## 📐 核心開發邏輯

### 1. 均勻點雲生成 (Fibonacci Sphere Algorithm)
為了避免點在球體兩極過於擁擠，我們採用斐波那契螺旋演算法，確保 $N$ 個點在球面上完美均勻分佈。

### 2. 手勢控制映射
*   **動態縮放 (Zoom)**：偵測「大拇指尖 (Landmark 4)」與「食指尖 (Landmark 8)」之距離。
*   **空間旋轉 (Rotation)**：追蹤「手掌中心」在水平 ($x$) 與垂直 ($y$) 方向的偏移量。
*   **3D 視覺模擬**：根據 $z$ 軸深度調整點的大小與亮度，營造 3D 立體感。

---

## 🚀 快速開始 (Quick Start)

### 1. 環境初始化
在專案根目錄開啟終端機（VS Code Terminal），執行以下指令：
```bash
# 建立虛擬環境
python -m venv .venv

# 啟動虛擬環境 (Windows)
.venv\Scripts\activate

# 安裝核心套件
pip install opencv-python mediapipe numpy
```

### 2. 開發階段 (Development Roadmap)
- [ ] **Phase 1: 影像輸入** - 確保 OpenCV 能正常驅動 ASUS X515 前鏡頭。
- [ ] **Phase 2: 手勢解析** - 整合 MediaPipe 並取得手部 21 個座標點。
- [ ] **Phase 3: 數學建模** - 實作 3D 旋轉矩陣與點雲投影公式。
- [ ] **Phase 4: 整合渲染** - 將手勢參數映射至球體，完成互動迴圈。

---

## 📁 專案架構 (Project Structure)
```text
GestureSphere/
├── .venv/               # Python 虛擬環境
├── main.py              # 進入點：整合影像處理與主迴圈
├── geometry.py          # 數學邏輯：存放球體演算法與矩陣運算
├── requirements.txt     # 套件清單
└── README.md            # 本說明文件
```

---

## 💡 開發備忘錄
*   **效能優化**：若畫面出現延遲，請將 `N` (點的數量) 降至 500 以下。
*   **Docker 說明**：目前優先使用 `venv` 開發以利鏡頭存取；未來若需 Docker 化，需解決 WSL2 對硬體裝置的掛載權限。
*   **互動設計**：建議加入平滑移動（Smoothing）機制，減少手部細微抖動對球體造成的閃爍。
---

這份文件已經預留了之後實作需要的數學邏輯框架。當你準備好動工寫程式碼時，隨時告訴我，我們從第一步開始！(๑•̀ㅂ•́)و✧