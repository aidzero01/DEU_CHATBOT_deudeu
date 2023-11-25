# 필요한 라이브러리를 임포트합니다.
from flask import Flask, render_template, request, jsonify
import pandas as pd
import random
import numpy as np  # 추가로 numpy 라이브러리를 임포트

app = Flask(__name__)

# 엑셀 파일 경로
excel_file_path = 'C:/teamproject/front_end/excel/file.xlsx'

# 엑셀 파일에서 데이터를 읽어옵니다.
df = pd.read_excel(excel_file_path,sheet_name='question')
df_menu = pd.read_excel(excel_file_path, sheet_name='menu', index_col='행긱')

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
        return row['답변'], row['부가설명']
    
    # 'menu' 시트에서 모든 행의 데이터 읽기
    elif "메뉴" in user_question or "학식" in user_question:
        # 모든 행의 레이블을 가져옵니다.
        menu_meals = df_menu.index.tolist()
        
        # 각 아침, 점심, 저녁 메뉴를 나눠서 문자열로 구성
        menu_data_list = []
        for meal in menu_meals:
            menu_items = df_menu.loc[meal].apply(str).values.flatten().tolist()
            menu_str = f"{meal}:\n{', '.join(menu_items)}\n"
            menu_data_list.append(menu_str)

        # 가져온 메뉴 정보를 줄바꿈으로 구분한 문자열로 반환
        menu_str = '\n'.join(menu_data_list)
        return menu_str, ''
    
    else:
        return '죄송합니다. 해당 질문에 대한 답변을 찾을 수 없습니다.', ''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
