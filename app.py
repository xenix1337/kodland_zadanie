import random

from flask import Flask, render_template,request
from sqlalchemy import select

from db import SessionLocal
from models import Question, QuizResult

app = Flask(__name__)


@app.route('/')
def index():
    session = SessionLocal()
    query = select(Question).limit(5)

    questions: list[dict] = []

    for question in session.execute(query).all():
        question: Question = question[0]

        answers = [question.valid_answer, question.answer_2, question.answer_3, question.answer_4]
        random.shuffle(answers)

        questions.append({
            'id': question.id,
            'question': question.question,
            'answers': answers
        })
    random.shuffle(questions)

    session.close()

    return render_template('index.html', questions=questions)

@app.route('/quiz', methods=['POST'])
def check_answers():
    questions_ids = [int(str(question).strip('question')) for question in request.json.keys() if str(question).startswith("question")]
    session = SessionLocal()
    query = select(Question).where(Question.id.in_(questions_ids))

    score: int = 0
    for question in session.execute(query).all():
        question: Question = question[0]

        given_answer = request.json[f'question{question.id}']
        valid_answer = question.valid_answer.strip().lower().replace(' ', '_')

        if given_answer == valid_answer:
            score += 1

    result: QuizResult = QuizResult(username=request.json['username'], score=score)
    session.add(result)
    session.commit()

    session.close()

    return {"score": score}


if __name__ == '__main__':
    app.run()
