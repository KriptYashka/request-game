from crypt import methods

from flask import Flask, render_template, Response, request, jsonify
from data import Game
import json

app = Flask(__name__)
header = {'Content-Type': 'text/html;charset=utf-8'}


@app.route('/')
def hello():
  return render_template('index.html')

@app.route('/question/<qid>', methods=["GET", "POST"])
def question_view(qid: str):
    data = Game.questions.data
    if qid not in data:
        error = f"Вопроса с id '{qid}' не существует."
        return Response(error, status=400)
    question = data[qid]
    description = question["question"]
    answers = question["answer"]
    score = question["score"]

    text = "<h2>Неверный метод запроса.</h2>"
    if request.method == "GET":
        text = f"<h2>Вопрос #{qid}<h2><hr>Награда за ответ: {score}<br>{description}"
    if request.method == "POST":
        keys = ["team", "answer"]
        response_body: dict[str, str] = {}
        missing_keys = []
        try:
            s = request.data.decode('utf8')
            request_json = json.loads(s)
        except:
            return Response("Ошибка перевода JSON в текст", status=400)
        for key in keys:
            if key not in request_json:
                missing_keys.append(key)
            else:
                response_body[key] = request_json[key]
        if missing_keys:
            return Response(f"В теле запроса отсутствуют следующие ключи: {missing_keys}")

        if response_body["answer"] in answers:
            code = Game.solve(qid, response_body["team"])
            if code == 1:
                text = "Ответ <b>правильный</b>!"
            elif code == -2:
                text = f"Команды {response_body['team']} не существует."
            elif code == -1:
                text = "Ответ правильный!<br>Ваша команда уже ответила на этот вопрос."

        elif response_body["answer"].lower() in map(lambda s: s.lower(), answers):
            text = "Обратите внимание на регистр. Это важно."
        else:
            text = "Ответ <b>неверный</b>!"

    return Response(text, status=200)


@app.route("/score/<team>", methods=["GET"])
def score_view(team: str):
    score = Game.get_score(team)
    if score == -2:
        return Response(f"Команды {team} не существует.", status=400)
    return Response(f"Счёт команды <b>{team.upper()}</b>: {score}")

@app.route("/field", methods=["GET", "POST"])
def field_view():
    if request.method == "GET":
        field = Game.field.field
        return Response(str(field), status=200)

    keys = ["team", "x", "y"]
    response_body: dict[str, str] = {}
    missing_keys = []
    try:
        s = request.data.decode('utf8')
        request_json = json.loads(s)
    except:
        return Response("Ошибка перевода JSON в текст", status=400)
    for key in keys:
        if key not in request_json:
            missing_keys.append(key)
        else:
            response_body[key] = request_json[key]
    if missing_keys:
        return Response(f"В теле запроса отсутствуют следующие ключи: {missing_keys}")

    x, y = int(response_body["x"]), int(response_body["y"])
    team = response_body["team"]

    code = Game.set_point(x, y, team)
    if code == -2:
        return Response(f"Команды {team} не существует.", status=400)
    elif code == -1:
        return Response(f"У вашей команды закончились очки.", status=200)
    elif code == 2:
        return Response(f"Клетка {x, y} уже захвачена вашей командой. Очки не потерялись. Осталось {Game.get_score(team)} очков")
    return Response(f"Клетка {x, y} захвачена. Осталось {Game.get_score(team)} очков")

def main():
    app.run()

if __name__ == '__main__':
    main()
