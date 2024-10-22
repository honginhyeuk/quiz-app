from flask import Flask, render_template, request, redirect, url_for
import json
import os
import random

app = Flask(__name__)

# JSON 파일 로드 함수
def load_quiz_data():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    json_path = os.path.join(base_dir, 'quiz_data_sap_fi.json')
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

quiz_data = load_quiz_data()
random.shuffle(quiz_data)
wrong_answers = []  # 오답 문제를 저장할 리스트

@app.route("/", methods=["GET", "POST"])
def quiz():
    # URL에서 question_index 가져오기, 기본값은 0
    question_index = int(request.args.get("question_index", 0))
    result = request.args.get("result", "")

    if request.method == "POST":
        # 사용자가 제출한 답변 가져오기
        user_answers = request.form.getlist("answer")
        correct_answers = quiz_data[question_index]['infoAnswer']

        # 정답 여부 판단
        if sorted(user_answers) == sorted(correct_answers):
            result = "정답입니다!"
        else:
            result = f"오답입니다! 정답은 {', '.join(correct_answers)}입니다."
            # 중복 방지를 위해 인덱스가 이미 존재하는지 확인
            if question_index not in wrong_answers:
                wrong_answers.append(question_index)

        # 리다이렉트로 결과 전달
        return redirect(url_for('quiz', question_index=question_index, result=result))

    # 모든 문제를 푼 경우 오답 문제로 이동
    if question_index >= len(quiz_data):
        if wrong_answers:
            question_index = wrong_answers.pop(0)  # 오답 문제로 이동
        else:
            return render_template("end.html")  # 모든 문제 완료 시 종료 화면

    # 다음 질문을 위한 선택지 준비
    choices = [(chr(65 + i), choice) for i, choice in enumerate(quiz_data[question_index]['infoChoice'])]

    # 템플릿 렌더링
    return render_template(
        "quiz.html",
        choices=choices,
        question=quiz_data[question_index],
        question_index=question_index,
        result=result,
        quiz_length=len(quiz_data) + len(wrong_answers)  # 총 질문 수 + 오답 수
    )

if __name__ == '__main__':
    app.run()
