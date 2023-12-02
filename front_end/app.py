# 필요한 라이브러리를 임포트합니다.
from flask import Flask, render_template, request, jsonify
import pandas as pd
import random
import datetime
import numpy as np  # 추가로 numpy 라이브러리를 임포트

app = Flask(__name__)

# 엑셀 파일 경로
excel_file_path = 'C:/teamproject/front_end/excel/file.xlsx'

# 엑셀 파일에서 데이터를 읽어옵니다.
df = pd.read_excel(excel_file_path,sheet_name='question')
df_menu = pd.read_excel(excel_file_path, sheet_name='menu', index_col='행긱')
current_time = datetime.datetime.now()
weekday_dict = {
    0: '월',
    1: '화',
    2: '수',
    3: '목',
    4: '금',
    5: '토',
    6: '일'
}
current_day = weekday_dict[current_time.weekday()]
# 'menu' 시트의 인덱스 확인
print(df_menu.index)

@app.route('/')
def index():
    return render_template('index_scroll.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_question = request.form['user_question']
    response, additional_info = search_answer(user_question)

    # NaN이나 Infinity를 처리
    response = replace_nan(response)
    additional_info = replace_nan(additional_info)

    return jsonify({'response': response, 'additional_info': additional_info, 'question': user_question})

def replace_nan(value):
    # NaN이나 Infinity를 문자열로 변환
    if isinstance(value, (float, np.floating)):
        if np.isnan(value) or np.isinf(value):
            return 'NaN or Infinity'
    return value

def search_answer(user_question):
    # 'question' 시트에서 질문과 답변 정보 읽기
    question_row = df[df['질문'].str.lower().str.contains(user_question.lower(), na=False)]
    if not question_row.empty:
        row = question_row.iloc[random.randint(0, len(question_row)-1)]
        answer = row['답변']
        additional_info = row['부가설명']

        # 숫자나 다른 데이터 타입이면 문자열로 변환 후 처리
        if isinstance(answer, str):
            answer = answer.replace('\n', '<br>')  # 줄바꿈 처리
        if isinstance(additional_info, str):
            additional_info = additional_info.replace('\n', '<br>')

        return answer, additional_info
    
    # 'menu' 시트에서 행의 데이터 읽기
    elif "행긱" in user_question:
        menu_type_happy = get_menu_type_happy(user_question)
        menu_str = get_menu_happy(menu_type_happy)
        return menu_str, ''
        
    elif "효민" in user_question:
        menu_type_hyo = get_menu_type_hyo(user_question)
        menu_str = get_menu_hyo(menu_type_hyo)
        return menu_str, ''    
    
    else:
        return '죄송합니다. 해당 질문에 대한 답변을 찾을 수 없습니다.', ''

def get_menu_type_happy(user_question):
    if "아침" in user_question:
        return "아침(한식)","아침(일품)"
    elif "점심" in user_question:
        return "점심(한식)","점심(일품)"
    elif "저녁" in user_question:
        return "저녁(한식)","저녁(일품)"
    else:
        return None

def get_menu_happy(menu_type_happy):
    if menu_type_happy is not None:
        menu_str = f"[행복기숙사] - {current_time.strftime('%Y년 %m월 %d일') + ' ' + current_day}요일 :<br>\n"
        for menu_type in menu_type_happy:
            menu_items = str(df_menu.loc[menu_type, current_day]).split(',')
            menu_str += f"{menu_type} {' - '.join(menu_items)}<br>\n"
        return menu_str
    else:
        return '메뉴 타입을 찾을 수 없습니다.'

def get_menu_type_hyo(user_question):
    if "아침" in user_question:
        return "아침"
    elif "점심" in user_question:
        return "점심"
    elif "저녁" in user_question:
        return "저녁"
    else:
        return None

def get_menu_hyo(menu_type_hyo):
    if menu_type_hyo is not None:
        menu_items = df_menu.loc[menu_type_hyo, current_day].split(',')
        menu_str = f"[효민기숙사] - {menu_type_hyo} / {current_time.strftime('%Y년 %m월 %d일')} {weekday_dict[current_time.weekday()]}요일 :<br> \n"

        # Adding each menu item with a line break
        for item in menu_items:
            menu_str += f" {item.strip()}<br>"

        return menu_str
    else:
        return '메뉴 타입을 찾을 수 없습니다.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
