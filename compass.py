"""Pure demo logic. All clauses, dates and rates are fictional."""
import re

DOCUMENTS = [
    {'文件': 'CLM-001 理賠應備文件', '版本': 'v4', '狀態': '現行', '生效日': '2024-01-01', '負責單位': '理賠部', '建議動作': '維持現行'},
    {'文件': 'CLM-001 理賠應備文件', '版本': 'v2', '狀態': '已廢止', '生效日': '2021-01-01', '負責單位': '理賠部', '建議動作': '封存舊版本'},
    {'文件': 'POL-002 保單借款規範', '版本': 'v3', '狀態': '現行', '生效日': '2023-05-01', '負責單位': '保全部', '建議動作': '比對利率差異'},
    {'文件': 'POL-002 保單借款規範', '版本': 'v1', '狀態': '已廢止', '生效日': '2021-01-01', '負責單位': '保全部', '建議動作': '封存舊版本'},
    {'文件': 'POL-003 住所變更', '版本': 'v2', '狀態': '現行', '生效日': '2024-03-01', '負責單位': '保全部', '建議動作': '維持現行'},
    {'文件': 'IT-003 工單規範', '版本': 'v1', '狀態': '現行', '生效日': '2024-01-01', '負責單位': 'IT 服務台', '建議動作': '補齊環境資訊'},
]

def answer(question, role='一般員工', knowledge=None):
    q = question.strip()
    result = {'question': q, 'role': role, 'text': '', 'citations': [], 'source': '—', 'validity': '未引用文件', 'conflict': '未發現', 'matched': False, 'escalate': False}
    def cite(doc, version, article, body):
        result.update(source=doc + ' · ' + article, validity='只採用現行版', matched=True)
        result['citations'].append({'id': doc, 'version': version, 'article': article, 'body': body})
    # Restricted topics never read from the user-added demo knowledge.
    if re.search('核保|機密', q):
        result['text'] = ('**角色符合，但目前未載入核保內規，無法提供可靠回答。**' if role == '核保人員' else '**此問題涉及受限制的核保知識。**\n\n此示範角色不可讀取機密核保內規，請洽核保部門。')
        result['conflict'] = '權限／資料把關'
    elif knowledge and q in knowledge:
        result['text'] = '**已確認的專家知識**\n\n' + knowledge[q]
        cite('SOP-DEMO', 'v1', '專家確認紀錄', knowledge[q])
    elif re.search('借款|利率', q):
        result['text'] = '**示範條文中的保單借款利率上限為 6.25%。**\n\n採用 2023-05-01 生效的 v3；2021 年 v1 已於 2023-04-30 廢止。此利率為虛構資料，非實際商品條件。'
        result['conflict'] = '已排除廢止版'
        result['versions'] = [{'版本': '2021 / v1', '利率上限': '7.5%', '狀態': '已廢止'}, {'版本': '2023 / v3', '利率上限': '6.25%', '狀態': '現行'}]
        cite('POL-002', 'v3', '第 5 條', '本示範規範之保單借款利率上限為年利率 6.25%。')
    elif re.search('理賠|給付', q):
        result['text'] = '**先確認申請的是身故理賠或醫療理賠。**\n\n- 共同文件：申請書、身分證明、收款帳戶資料。\n- 身故理賠：另附死亡證明與受益人相關證明。\n- 醫療理賠：另附診斷證明、醫療收據與費用明細。\n\n口語對應：辦理賠 → 保險金給付；準備什麼 → 應備文件。'
        result['conflict'] = '已排除 v2'
        cite('CLM-001', 'v4', '第 3、4 條', '依申請類型檢附上述示範文件。實際應備文件須依商品與公司現行規定確認。')
    elif re.search('地址|住所', q):
        result['text'] = '**客戶改地址，對應「保全變更－住所變更」。**\n\n1. 確認要保人身分。\n2. 填寫住所變更申請資料。\n3. 核對文件後由保全單位辦理。'
        cite('POL-003', 'v2', '第 2 條', '住所變更需核驗要保人身分，提交變更申請後交由保全單位處理。')
    elif re.search('VPN|密碼|帳號|IT|連線', q, re.I):
        result['text'] = '**這是 IT 支援問題，我可以幫你分流。**\n\n請前往側欄的「IT 支援與代辦」，提供問題類型與錯誤代碼。'
        cite('IT-003', 'v1', '第 2 條', '工單需包含問題分類、錯誤代碼、作業系統、已試步驟與相關文件。')
    else:
        result['text'] = '**目前知識庫沒有足夠依據，無法可靠回答。**\n\n我不會推測不存在的規定。你可以把問題加入待專家回覆清單。'
        result['escalate'] = True
    return result


def triage(issue, code, os_name, tried=''):
    code = code.strip().upper()
    if not code:
        raise ValueError('錯誤代碼或訊息不可空白')
    auto = issue in ['密碼到期', '帳號被鎖定'] or (issue == 'VPN 無法連線' and code == 'E-809')
    actions = {'密碼到期': '發起密碼重設', '帳號被鎖定': '解鎖帳號', 'VPN 無法連線': '推送 VPN 用戶端更新'}
    return {'auto': auto, 'action': actions.get(issue, '轉交服務台') if auto else '轉交服務台', 'issue': issue, 'code': code, 'os': os_name, 'tried': tried.strip() or '未提供', 'source': 'IT-003 v1 第 2 條', 'demo': True}
