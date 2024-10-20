import json
import re
from docx import Document

# 변환할 데이터를 저장할 리스트
quiz_data = []

# Word 파일을 읽고 각 문제의 패턴을 추출
def process_question_block(block):
    # 문제와 선택지, 답을 추출하기 위한 정규 표현식
    question_pattern = r"(NO\.\d+)\s*(.*?)\s*(A\..*?)Answer:\s*(.*)"
    match = re.search(question_pattern, block, re.DOTALL)
    if match:
        number = match.group(1).replace("NO.", "").strip()
        question = match.group(2).strip()

        # 선택지 구문 처리
        choices = match.group(3).strip().splitlines()
        formatted_choices = []
        for choice in choices:
            if ". " in choice:
                formatted_choices.append(choice.split(". ", 1)[1])
            else:
                formatted_choices.append(choice)  # 점(.)과 공백이 없을 경우 전체 텍스트 추가

        # 답 구문 처리
        answer = match.group(4).strip()
        
        # 쉼표와 공백을 제거한 답 리스트 처리
        answer = re.sub(r'[,\s]', '', answer)  # 쉼표와 공백을 모두 제거
        if len(answer) > 1:
            answer = list(answer)  # 여러 개의 답이 있을 경우 리스트로 처리
        else:
            answer = answer  # 하나의 답일 경우 문자열로 처리

        # JSON 포맷으로 추가
        quiz_data.append({
            "infoType": "SAP FI",
            "infoTime": "SAP FI",
            "infoNumber": number,
            "infoQuestion": question,
            "infoChoice": formatted_choices,
            "infoAnswer": answer,
            "infoDesc": ""  # 설명은 기본적으로 비어있도록 처리
        })

# Word 파일에서 텍스트를 읽는 함수
def read_word_file(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)

# Word 파일에서 텍스트 읽기
file_path = 'C:/Users/inheu/Downloads/C_TS4FI_통합 번역 ONLY영어버전 (2).docx'  # Word 파일 경로 설정
word_text = read_word_file(file_path)

# 문제 구간으로 분리
question_blocks = word_text.split("NO.")  # 각 문제는 "NO."로 시작하므로 분리

# 각 블록을 처리하여 JSON으로 변환
for block in question_blocks[1:]:
    process_question_block("NO." + block)

# JSON 파일로 저장
output_path = "C:/Users/inheu/sap fi quiz/quiz_data_sap_fi.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(quiz_data, f, indent=4, ensure_ascii=False)

print(f"JSON 파일이 {output_path}에 저장되었습니다.")
