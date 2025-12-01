import streamlit as st
import google.generativeai as genai
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image
import os
import traceback

# 1. 設定頁面 (必須是第一個 Streamlit 指令)
st.set_page_config(
    page_title="泰和茂智能工安系統",
    page_icon="🏗️",
    layout="wide"
)

# 2. 設定 Gemini API
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# 3. 自訂 CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    .promise-box {
        background: white;
        padding: 1.5rem;
        border-left: 5px solid #2a5298;
        margin: 1rem 0;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .promise-item {
        font-size: 1.1rem;
        margin: 0.5rem 0;
        color: #1e3c72;
        font-weight: 500;
    }
    .result-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid #e9ecef;
    }
    .footer {
        text-align: center;
        padding: 2rem;
        color: #6c757d;
        border-top: 1px solid #dee2e6;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# 4. 主畫面標題區域
st.markdown("""
<div class="main-header">
    <div class="main-title">🏗️ 泰和茂智能工安系統</div>
    <div class="subtitle">泰和茂營建團隊 | 和固營造有限公司</div>
    <div style="margin-top: 1rem; font-size: 0.9rem;">用 AI 守護每一個工地承諾</div>
</div>
""", unsafe_allow_html=True)

# 5. 三大承諾區域
st.markdown("""
<div class="promise-box">
    <h3 style="color: #1e3c72; margin-bottom: 1rem;">泰和茂三大核心承諾</h3>
    <div class="promise-item">✓ 不偷工減料</div>
    <div class="promise-item">✓ 不延誤工期</div>
    <div class="promise-item">✓ 不發生工安意外</div>
</div>
""", unsafe_allow_html=True)

# 6. 側邊欄設定
with st.sidebar:
    # --- LOGO 智慧顯示區 ---
    # 程式碼將檢查同資料夾中是否存在 "logo.png" 檔案
    if os.path.exists("logo.png"):
        st.image("logo.png", width="stretch")
    else:
        # 備用圖片 (如果找不到 logo.png)
        st.image("https://placehold.co/600x200/1e3c72/ffffff/png?text=Taihe+Mao+Group", width="stretch")
        if not os.path.exists("logo.png"):
             st.caption("💡 提示：請將您的圖片改名為 **logo.png** 並放入同資料夾中即可顯示。")
    
    st.markdown("---")
    
    st.markdown("### 📋 檢測模式")
    check_mode = st.radio(
        "選擇檢測類型",
        ["🛡️ 工安檢測", "⚙️ 品質檢測", "📊 進度記錄"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ API 設定")
    
    if not GEMINI_API_KEY:
        api_key_input = st.text_input("請輸入 Gemini API Key", type="password")
        if api_key_input:
            genai.configure(api_key=api_key_input)
            st.success("✓ API Key 已設定")
    else:
        st.success("✓ API Key 已配置")
    
    st.markdown("---")
    st.markdown("""
    ### 📞 聯絡資訊
    **泰和茂營建團隊** 和固營造有限公司  
    地址：彰化縣彰化市辭修路203號
    """)

# 7. 主要功能分頁
tab1, tab2, tab3 = st.tabs(["📸 上傳檢測", "📊 檢測報告", "ℹ️ 使用說明"])

with tab1:
    st.markdown("### 📸 上傳工地照片進行檢測")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "拍攝或上傳工地照片",
            type=['jpg', 'jpeg', 'png'],
            help="支援 JPG、JPEG、PNG 格式"
        )
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="已上傳的照片", width="stretch")
    
    with col2:
        st.markdown("#### 📝 檢測資訊")
        project_name = st.text_input("專案名稱", placeholder="例：涵森 3F 施工區")
        inspector_name = st.text_input("檢測人員", placeholder="例：王大明")
        location = st.text_input("檢測位置", placeholder="例：3樓東側")
        
    if uploaded_file and st.button("🚀 開始 AI 檢測", type="primary", use_container_width=True):
        
        # 定義 Prompt (提示詞)
        if check_mode == "🛡️ 工安檢測":
            prompt = f"""你是泰和茂營造的 AI 工安檢測助手。
泰和茂堅持「不偷工減料、不延誤工期、不發生工安意外」三大承諾，其中「不發生工安意外」是最高優先。

請仔細分析這張工地照片，進行全面的工安檢測。
【重要】請特別注意：
1. 請先仔細數一數照片中有幾個人
2. 逐一檢查每個人，不要遺漏任何一個人
3. 如果有人沒戴安全帽，請明確指出該人的位置
4. 請用放大鏡般的仔細程度檢查每個細節

檢測項目：
1. 所有人員是否配戴安全帽？
2. 是否穿著反光背心？
3. 高處作業人員是否使用安全帶？
4. 是否穿著安全鞋？
5. 施工區域是否有完整圍欄？
6. 警示標誌是否清晰可見？
7. 鷹架是否穩固？有無護欄？
8. 逃生通道是否暢通？
9. 滅火器位置是否正確？
10. 電線是否整理妥善？有無拖地？
11. 材料堆放是否整齊穩固？
12. 是否有明顯的危險區域？
13. 施工機具是否有定期檢查標籤？

請用以下格式回答：
## 檢測結果總覽
- 照片中人數：X 人
- 整體安全評級：[A/B/C/D]
- 發現問題數量：X 項
## 詳細檢測項目
### ✅ 符合項目
### ❌ 違規項目（需立即改善）
### ⚠️ 注意事項（建議改善）
### 🔍 無法判斷項目
## 改善建議
## 泰和茂品質標準評語
"""
        elif check_mode == "⚙️ 品質檢測":
            prompt = f"""你是泰和茂營造的 AI 品質檢測助手。
泰和茂堅持「不偷工減料」承諾。
標準：3000磅台菘水泥、筏式基礎、耐震螺旋鋼筋、全棟防水。

請分析照片進行品質檢測：
1. 混凝土表面是否平整？有無蜂窩、裂縫？
2. 鋼筋綁紮是否確實？間距是否符合？
3. 防水施作是否確實？
4. 建材品質與環境整潔？

請用以下格式回答：
## 品質檢測總覽
- 整體品質評級：[A/B/C/D]
- 發現問題數量：X 項
## 詳細檢測項目
### ✅ 符合標準項目
### ❌ 不合格項目
### ⚠️ 待改進項目
### 🔍 無法判斷項目
## 改善建議
## 泰和茂品質標準評語
"""
        else:  # 進度記錄
            prompt = f"""你是泰和茂營造的 AI 進度記錄助手。
泰和茂堅持「不延誤工期」承諾。

請分析照片記錄進度：
1. 目前處於什麼施工階段？
2. 具體工項是什麼？
3. 完成度評估？
4. 人力與設備是否充足？
5. 潛在延誤因素？

請用以下格式回答：
## 進度記錄總覽
- 施工階段：[名稱]
- 完成度：X%
- 進度狀態：[正常/稍慢/延誤]
## 詳細進度分析
### 📍 當前工作項目
### 📈 完成情況
### 👷 人力與資源
### ⚠️ 潛在風險
## 進度建議
## 泰和茂工期管理評語
"""

        with st.spinner('🤖 AI 正在分析照片中... (自動選擇最佳模型)'):
            try:
                # 圖片轉檔
                img_byte_arr = BytesIO()
                image.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                
                # --- 自動修復機制：根據您的帳號權限更新模型列表 ---
                models_to_try = [
                    'gemini-2.5-flash',       # 優先：最新的 2.5 Flash
                    'gemini-2.0-flash',       # 備用：穩定的 2.0 Flash
                    'gemini-flash-latest',    # 保底：指向最新 Flash 版本
                ]
                
                response = None
                last_error = None
                success_model = ""

                # 迴圈嘗試可用的模型
                for model_name in models_to_try:
                    try:
                        model = genai.GenerativeModel(model_name)
                        response = model.generate_content([
                            prompt,
                            {
                                'mime_type': 'image/png',
                                'data': img_byte_arr
                            }
                        ])
                        success_model = model_name
                        break # 成功則跳出
                    except Exception as e:
                        last_error = e
                        # 繼續嘗試下一個
                        continue
                
                # 若所有模型都失敗
                if response is None:
                    raise Exception(f"所有模型嘗試皆失敗。最後錯誤: {last_error}")

                # --- 成功 ---
                st.success(f"✅ 檢測完成！(使用模型: {success_model})")
                
                st.markdown("---")
                
                # 資訊卡片
                info_col1, info_col2, info_col3, info_col4 = st.columns(4)
                with info_col1:
                    st.metric("檢測時間", datetime.now().strftime("%H:%M"))
                with info_col2:
                    st.metric("專案名稱", project_name if project_name else "未填寫")
                with info_col3:
                    st.metric("檢測人員", inspector_name if inspector_name else "未填寫")
                with info_col4:
                    st.metric("檢測位置", location if location else "未填寫")
                
                st.markdown("---")
                
                # 顯示結果
                st.markdown("### 📋 AI 檢測報告")
                st.markdown(f'<div class="result-box">{response.text}</div>', unsafe_allow_html=True)
                
                # 儲存記錄
                if 'reports' not in st.session_state:
                    st.session_state.reports = []
                
                report_data = {
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'mode': check_mode,
                    'project': project_name,
                    'inspector': inspector_name,
                    'location': location,
                    'result': response.text,
                    'image': image
                }
                st.session_state.reports.append(report_data)
                
                # 下載按鈕
                st.markdown("---")
                col_dl1, col_dl2 = st.columns(2)
                with col_dl1:
                    report_text = f"""
泰和茂智能工安系統 - 檢測報告
{'='*60}
檢測時間：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
專案名稱：{project_name if project_name else '未填寫'}
檢測人員：{inspector_name if inspector_name else '未填寫'}
使用模型：{success_model}
{'='*60}
{response.text}
"""
                    st.download_button(
                        label="📥 下載文字報告",
                        data=report_text,
                        file_name=f"泰和茂檢測報告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                
            except Exception as e:
                st.error(f"❌ 檢測失敗")
                st.error(f"錯誤訊息: {str(e)}")
                with st.expander("🔍 開發者除錯資訊"):
                    st.code(traceback.format_exc())

with tab2:
    st.markdown("### 📊 歷史檢測報告")
    if 'reports' in st.session_state and len(st.session_state.reports) > 0:
        st.success(f"✅ 共有 {len(st.session_state.reports)} 筆檢測記錄")
        for idx, report in enumerate(reversed(st.session_state.reports)):
            with st.expander(f"📋 {report['timestamp']} - {report['mode']} - {report['project']}"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    if report['image']:
                        st.image(report['image'], caption="檢測照片", width="stretch")
                with col2:
                    st.markdown("**檢測結果**")
                    st.markdown(report['result'])
    else:
        st.info("📭 尚無檢測記錄")

with tab3:
    st.markdown("### ℹ️ 系統使用說明")
    st.markdown("本系統專為泰和茂營建團隊設計，運用 AI 技術協助工地管理。")

st.markdown("""
<div class="footer">
    <strong>泰和茂智能工安系統 v1.6 (PNG Optimized)</strong><br>
    <small>© 2025 Developed by Carson Liu</small>
</div>
""", unsafe_allow_html=True)