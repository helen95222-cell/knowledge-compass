# 知識羅盤 Knowledge Compass

依初賽企劃書 v3 製作的 Streamlit 競賽互動原型。沿用深綠與米白風格。

功能：智慧問答與條號引用、廢止版本比對、模擬角色把關、知識健康度、IT 分流與模擬代辦、預填工單下載、專家 SOP 草稿與人工確認入庫。

## 部署到 Streamlit Community Cloud

1. 在 GitHub 建立儲存庫，建議名稱 `knowledge-compass`。
2. 將此 ZIP 解壓縮。進入 `knowledge-compass-streamlit` 資料夾，將**裡面的檔案**上傳到儲存庫根目錄；不要只上傳 ZIP。
3. 確認根目錄至少包含 `app.py`、`compass.py`、`requirements.txt`。`.streamlit/config.toml` 提供品牌配色；若拖曳上傳時未包含隱藏資料夾，可在 GitHub 用 Add file → Create new file 建立 `.streamlit/config.toml`，貼入設定內容。
4. 開啟 https://share.streamlit.io ，登入並連接你的 GitHub。
5. 點選 **Create app** → **Yup, I have an app.**
6. Repository：`你的帳號/knowledge-compass`；Branch：`main`；Main file path：`app.py`。
7. App URL 可填 `knowledge-compass`；如果已被使用，改為其他名稱，例如 `knowledge-compass-helen`。是否可用以平台結果為準。
8. 按 **Deploy**。完成後使用平台實際回傳的 `https://名稱.streamlit.app` 網址分享。

Streamlit 不是 `streamlit.io` 下的自訂網站網址；Community Cloud 應用部署在 `streamlit.app` 子網域。
若要讓評審直接開啟，請在 App settings 的 Sharing 確認觀眾存取設定。不要為此上傳任何真實內部文件。

官方說明：https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

## 本機啟動

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## 展示路線（約 3 分鐘）

1. 智慧助手：點選理賠問題，展開引用，查看右側治理面板。
2. 問保單借款利率：比較舊版 7.5% 與現行 6.25%，解釋過期文件把關。
3. 以一般員工詢問機密核保內規：展示權限限制；切換核保角色後仍拒答，因示範庫未包含內規。
4. IT 支援：VPN + E-809 展示模擬代辦；VPN + E-700 展示預填工單與 JSON 下載。
5. 在助手輸入未收錄問題（例如「新人第一天去哪裡領識別證？」），加入專家清單。
6. 知識飛輪：填寫示範專家回覆、儲存草稿、人工確認入庫；返回助手詢問完全相同問題，展示新知識回答。
7. 知識健康度：篩選現行與已廢止文件。

## 範圍與資料

- 所有保險條文、日期與利率均為虛構展示資料。
- 不依賴 API 金鑰，未串接 LLM、RAG、ITSM、真實企業資料或正式核身。
- 關鍵字匹配只能回答有限展示情境；不是任意問題都能理解的 AI。
- 示範角色不是正式存取控制；受限制題目不會讀取專家入庫資料。
- 所有互動資料存於 `st.session_state`，不同訪客彼此隔離。重新載入、工作階段中斷或服務重啟可能清除。需要保留時請匯出 JSON。
- SOP 草稿與入庫是提案下一階段的延伸展示；不是已串接的正式知識治理流程。
- 本專案沒有重現或驗證簡報的 68 題評測數據。
