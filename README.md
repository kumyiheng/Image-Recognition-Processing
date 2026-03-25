# Image-Recognition-Processing
大三上多媒體技術概論期末報告

## 專案簡介
這是一個使用 Python 開發的 Line 機器人專案，旨在提供使用者一個簡單的介面來進行即時的影像處理。使用者只需在 Line 對話框中傳送圖片，即可透過選單指令套用各種濾鏡、去背或更換背景。

## 主要功能
- **自動儲存與暫存**：接收使用者傳送的 `.jpg` 圖片並儲存於伺服器。
- **智慧去背 (Background Removal)**：一鍵移除圖片背景，生成透明 PNG 檔。
- **多元濾鏡效果**：
  - 季節風格：冬天、夏天。
  - 藝術風格：復古、日系、卡通、素描、色鉛筆、底片相機。
  - 基本處理：黑白、灰階。
- **邊緣偵測 (Edge Detection)**：提取影像輪廓。
- **換背景功能 (Change Background)**：支援結合去背影像與新背景圖。
- **自動化清理**：內建腳本可定期清理暫存的影像檔案。
- **雲端整合**：處理完後的影像會自動上傳至 Imgur，並回傳連結給使用者。

## 技術棧 (Tech Stack)
- **語言**：Python 3.10
- **框架**：Flask (Webhook Server)
- **API 整合**：Line Bot SDK, Imgur API
- **影像處理**：OpenCV (cv2), Pillow (PIL), NumPy, SciPy
- **部署工具**：Ngrok (本地測試環境映射)

## 檔案結構說明
- `app.py`: 專案主程式，負責處理 Line 訊息邏輯。
- `bg.py`: 呼叫 `backgroundremover` 進行去背。
- `filter.py`: 核心濾鏡演算法（包含 10 種不同濾鏡）。
- `upload.py`: 串接 Imgur API 上傳處理後的圖片。
- `sketch.py` / `edge.py` / `blur.py`: 個別影像效果實作。
- `deljpg.py` / `delpng.py`: 清理暫存檔的輔助腳本。
