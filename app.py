"""Knowledge Compass: competition demo; no real insurance or IT integrations."""
import json
from datetime import datetime
import streamlit as st
from compass import answer, triage, DOCUMENTS

st.set_page_config(page_title='知識羅盤｜Knowledge Compass', page_icon='🧭', layout='wide')
st.markdown('''<style>
.stApp {background:#f5f7f3;color:#234b3b}
h1,h2,h3 {color:#124f40 !important}
[data-testid="stSidebar"] {background:#edf3e8}
[data-testid="stMetric"] {background:white;border:1px solid #dce5d9;padding:18px;border-radius:12px}
.stButton>button {border-radius:9px}
[data-testid="stChatMessage"] {border:1px solid #e0e6df;border-radius:12px}
.block-container {padding-top:2.5rem}
</style>''', unsafe_allow_html=True)
for key, default in [('messages', []), ('queue', []), ('knowledge', {}), ('tickets', []), ('governance', None), ('it_plan', None)]:
    if key not in st.session_state:
        st.session_state[key] = default

with st.sidebar:
    st.title('✥ 知識羅盤')
    st.caption('KNOWLEDGE COMPASS')
    page = st.radio('工作區', ['智慧知識助手', '知識健康度', 'IT 支援與代辦', '知識飛輪', '關於此原型'])
    role = st.selectbox('模擬使用者角色', ['一般員工', '核保人員', '知識管理者'])
    st.divider()
    st.info('可信任 · 會成長 · 能代辦')
    st.caption('競賽互動展示｜條文均為虛構\n\n角色切換不是正式存取控制。')


def show_answer(result, index):
    st.markdown(result['text'])
    for citation in result['citations']:
        with st.expander(f"來源：{citation['id']} · {citation['version']} · {citation['article']}"):
            st.write(citation['body'])
            st.caption('模擬條文｜不可作為實際保險作業依據')
    if result.get('versions'):
        st.warning('偵測到版本差異，已排除廢止條文。')
        st.table(result['versions'])
    if result.get('escalate'):
        if st.button('加入待專家回覆清單 →', key=f'escalate_{index}'):
            q = result['question']
            if not any(x['question'] == q for x in st.session_state.queue):
                st.session_state.queue.append({'question': q, 'status': '待回覆', 'reply': ''})
            st.success('已加入此工作階段的專家清單，請前往「知識飛輪」。')

if page == '智慧知識助手':
    st.title('每一個問題，都有可靠的方向。')
    st.caption('用你的話提問，找到答案、確認來源，走向下一步。')
    chat, governance = st.columns([2.4, 1], gap='large')
    with chat:
        choices = ['客戶要辦理賠，我該請他準備什麼？', '保單借款的利率上限是多少？', '客戶要改地址，要怎麼辦？', 'VPN 連不上怎麼辦？']
        selected = None
        with st.expander('試試這些展示情境', expanded=not st.session_state.messages):
            for i, q in enumerate(choices):
                if st.button('↗ ' + q, key=f'example_{i}', width='stretch'):
                    selected = q
        prompt = st.chat_input('輸入你的問題…', max_chars=600)
        question = selected or prompt
        if question:
            result = answer(question, role, st.session_state.knowledge)
            st.session_state.messages.append({'question': question, 'answer': result, 'role': role})
            st.session_state.governance = result
        if not st.session_state.messages:
            st.info('從保險作業到 IT 問題，一個入口就夠。請點選展示情境或輸入問題。')
        for i, msg in enumerate(st.session_state.messages):
            with st.chat_message('user'):
                st.write(msg['question'])
            with st.chat_message('assistant', avatar='🧭'):
                st.caption('查詢時的示範角色：' + msg['role'])
                show_answer(msg['answer'], i)
    with governance:
        st.subheader('◈ 回答治理面板')
        g = st.session_state.governance
        st.write('目前角色：**' + role + '**')
        if g:
            st.write('上一筆查詢角色：**' + g['role'] + '**')
            st.write('引用來源：**' + g['source'] + '**')
            st.write('時效檢查：**' + g['validity'] + '**')
            st.write('版本衝突：**' + g['conflict'] + '**')
            st.write('檢索狀態：**' + ('命中示範資料' if g['matched'] else '無可靠依據') + '**')
        else:
            st.caption('等待提問後顯示來源與檢查結果。')
        st.divider()
        st.markdown('**四道知識把關**\n\n✓ 角色與密等\n\n✓ 生效與廢止\n\n✓ 版本差異\n\n✓ 查無依據就拒答')
        st.caption('此處是關鍵字規則判定，非 LLM 信心分數。')

elif page == '知識健康度':
    st.title('知識健康度')
    st.caption('看見知識庫的缺口，讓可靠的答案持續生長。')
    for col, label, value in zip(st.columns(4), ['展示文件', '現行版本', '廢止文件', '版本衝突'], [6, 4, 2, 2]):
        col.metric(label, value)
    status = st.selectbox('篩選文件', ['全部', '現行', '已廢止'])
    st.dataframe([d for d in DOCUMENTS if status == '全部' or d['狀態'] == status], width='stretch', hide_index=True)
    st.warning('借款利率與理賠條文皆為提案虛構資料，不可作為實際作業依據。')
    st.caption('此清單為網站的固定示範文件；專家入庫資料另列於「知識飛輪」。')

elif page == 'IT 支援與代辦':
    st.title('IT 支援，從回答到行動。')
    st.caption('兩個問題快速分流：可處理的模擬代辦，其餘預填工單。')
    left, right = st.columns(2, gap='large')
    with left:
        with st.form('it_triage'):
            st.subheader('01 / 描述你的問題')
            issue = st.selectbox('遇到什麼狀況？', ['VPN 無法連線', '密碼到期', '帳號被鎖定', '其他 IT 問題'])
            code = st.text_input('錯誤代碼 / 訊息', placeholder='例如 E-809、E-700；無代碼可輸入「無」', max_chars=100)
            os_name = st.selectbox('作業系統', ['Windows 11', 'Windows 10', 'macOS', '其他'])
            tried = st.text_input('已嘗試步驟（選填）', max_chars=500)
            if st.form_submit_button('開始分流 →', type='primary'):
                if not code.strip():
                    st.error('請提供錯誤代碼或輸入「無」。')
                else:
                    st.session_state.it_plan = triage(issue, code, os_name, tried)
    with right:
        st.subheader('02 / 建議處理路徑')
        plan = st.session_state.it_plan
        if not plan:
            st.info('完成左側資訊後，查看分流結果與下一步。')
        elif plan['auto']:
            st.success('命中可模擬代辦規則：' + plan['action'])
            st.info('只展示流程，不會更動真實帳號或裝置。')
            if st.button('確認模擬執行', disabled=plan.get('done', False), type='primary'):
                plan['done'] = True
                st.rerun()
            if plan.get('done'):
                st.success('模擬流程已完成。正式代辦需串接 IT 系統與核身流程。')
        else:
            st.warning('需轉交 IT 服務台；工單資訊已預填。')
            st.json({k: plan[k] for k in ['issue', 'code', 'os', 'tried', 'source']})
            if st.button('建立示範工單', disabled=plan.get('done', False), type='primary'):
                plan['done'] = True
                plan['ticket_id'] = 'DEMO-' + datetime.now().strftime('%Y%m%d%H%M%S%f')
                st.session_state.tickets.append(dict(plan))
                st.rerun()
            if plan.get('done'):
                st.success('已建立 ' + plan['ticket_id'] + '；未送至服務台。')
                st.download_button('下載工單 JSON', json.dumps(plan, ensure_ascii=False, indent=2), file_name=plan['ticket_id'] + '.json', mime='application/json')
    if st.session_state.tickets:
        with st.expander('本次工作階段的工單紀錄'):
            st.dataframe([{'編號': x['ticket_id'], '問題': x['issue'], '錯誤代碼': x['code']} for x in st.session_state.tickets], hide_index=True)

elif page == '知識飛輪':
    st.title('今天的未知，成為明天的知識。')
    st.caption('拒答 → 專家回覆 → SOP 草稿 → 人工確認 → 示範入庫')
    if not st.session_state.queue:
        st.info('目前沒有待回覆問題。請在助手中詢問示範資料以外的問題，再點選轉交專家。')
    for i, item in enumerate(st.session_state.queue):
        with st.container(border=True):
            st.subheader(item['question'])
            st.caption('狀態：' + item['status'])
            if item['status'] == '已入庫':
                st.write(item['reply'])
            else:
                with st.form(f'reply_form_{i}'):
                    reply = st.text_area('示範專家回覆 / SOP 草稿', value=item['reply'], max_chars=5000)
                    a, b = st.columns(2)
                    draft = a.form_submit_button('儲存 SOP 草稿')
                    approve = b.form_submit_button('人工確認並加入知識庫', type='primary')
                    if draft or approve:
                        if not reply.strip():
                            st.error('請先填寫專家回覆。')
                        else:
                            item['reply'] = reply.strip()
                            item['status'] = '已入庫' if approve else '待確認'
                            if approve:
                                st.session_state.knowledge[item['question']] = reply.strip()
                            st.rerun()
    st.caption('此流程不會寄送通知。入庫後，在助手詢問完全相同的問題，即可查到已確認的回覆。')
    st.download_button('匯出本次知識飛輪紀錄', json.dumps(st.session_state.queue, ensure_ascii=False, indent=2), file_name='knowledge-flywheel.json', mime='application/json')

else:
    st.title('答案敢用，知識會長，問題被做掉。')
    st.write('依「知識羅盤 初賽企劃書 v3」製作的競賽互動原型。')
    for col, title, body in zip(st.columns(3), ['可信任 Trust', '會成長 Grow', '能代辦 Act'], ['附文件與條號引用，排除廢止版本。', '誠實拒答，讓專家回覆沉澱成新知識。', 'IT 兩題分流，模擬代辦或預填工單。']):
        col.subheader(title)
        col.write(body)
    st.divider()
    st.markdown('''**原型範圍**
- 本網站使用固定示範資料與關鍵字規則，未串接 LLM、企業文件、ITSM 或正式核身。
- 角色切換僅供展示，並非正式權限控制。
- 簡報中的 68 題評測結果屬團隊原型自述，不是本網站的即時測量。
- 問答、草稿、入庫資料與工單僅保留於目前的 Streamlit 工作階段；重新載入、斷線或服務重啟後可能消失。不同訪客不共用資料。
- 請使用示範內容，勿輸入真實客戶、帳號或機密資訊。
''')
    confirm = st.checkbox('我確認要清除目前工作階段的所有示範紀錄')
    if st.button('重設示範紀錄', disabled=not confirm):
        for key in ['messages', 'queue', 'knowledge', 'tickets', 'governance', 'it_plan']:
            del st.session_state[key]
        st.rerun()
st.caption('2026 · KNOWLEDGE COMPASS / 企業知識與 IT 支援助手 · 競賽展示')
