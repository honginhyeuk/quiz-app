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


@app.route("/", methods=["GET", "POST"])
def quiz():

    # 질문의 순서를 무작위로 섞기
    quiz_data = random.shuffle(quiz_data)

    question_index = int(request.args.get("question_index", 0))
    result = request.args.get("result", "")

    if request.method == "POST":
        user_answers = request.form.getlist("answer")
        correct_answers = quiz_data[question_index]['infoAnswer']

        # 정답 여부 판단
        if sorted(user_answers) == sorted(correct_answers):
            result = "정답입니다!"
        else:
            result = f"오답입니다! 정답은 {', '.join(correct_answers)}입니다."

        return redirect(url_for('quiz', question_index=question_index, result=result))

    choices = [(chr(65 + i), choice) for i, choice in enumerate(quiz_data[question_index]['infoChoice'])]

    return render_template(
        "quiz.html",
        choices=choices,
        question=quiz_data[question_index],
        question_index=question_index,
        result=result,
        quiz_length=len(quiz_data)
    )

if __name__ == '__main__':
    app.run()
