# 필요한 라이브러리를 임포트합니다.
from flask import Flask, render_template, request, jsonify
import pandas as pd
import random
import numpy as np  # 추가로 numpy 라이브러리를 임포트

app = Flask(__name__)

# 엑셀 파일 경로
excel_file_path = 'C:/teamproject/front_end/excel/file.xlsx'

# 엑셀 파일에서 데이터를 읽어옵니다.
df = pd.read_excel(excel_file_path)

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
    question_row = df[df['질문'].str.lower().str.contains(user_question.lower(), na=False)]
    
    if not question_row.empty:
        
        row = question_row.iloc[random.randint(0, len(question_row)-1)]            
        return row['답변'], row['부가설명']
    else:
        return '죄송합니다. 해당 질문에 대한 답변을 찾을 수 없습니다.', ''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
