from flask import Flask, render_template, Response, request
from data import Game

app = Flask(__name__)

@app.route('/')
def hello():
  return render_template('index.html')

@app.route('/question/<qid>')
def question(qid: str):
    try:
        qid = int(qid)
    except TypeError as e:
        return Response("Parameter 'id' must be integer")
    if request.method == "GET":
        data =


def main():
    app.run()

if __name__ == '__main__':
    main()
