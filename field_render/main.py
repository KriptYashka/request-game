from raylib import colors
from pyray import *

import requests

class Settings:
    WIDTH, HEIGHT = 1420, 800
    FPS = 10
    URL = "https://kriptyashka.pythonanywhere.com/"

    padding = 20
    space = 2
    size_matrix = HEIGHT - 2 * padding
    RIGHT_SPLIT = size_matrix + padding

class Field:
    COLORS = {
        0: colors.GRAY,
        1: colors.RED,
        2: colors.GREEN,
        3: colors.BLUE
    }

    def __init__(self, url: str):
        self.data = []
        self.score = []
        self.url = url

    def load(self):
        try:
            data = requests.get(self.url)
            s = data.content.decode("utf8")
            field = eval(s)
            self.data = field
        except:
            print("Не удалось подключиться.")

    def draw(self):

        try:
            n, m = len(self.data[0]), len(self.data)
        except:
            return None

        size_cell = Settings.size_matrix // min(n, m)
        for y in range(n):
            for x in range(m):
                value = self.data[y][x]
                color = self.COLORS[value]
                cell = Rectangle(Settings.padding + x * size_cell, Settings.padding + y * size_cell,
                                 size_cell - Settings.space, size_cell - Settings.space)
                draw_rectangle_rec(cell, color)

    def get_score(self):
        score = {
            i: 0 for i in range(4)
        }
        for row in self.data:
            for val in row:
                score[val] += 1
        return score

class Text:
    def __init__(self, pos: list, color):
        self.pos = pos
        self.text = "No data"
        self.color = color
        self.__url = None

    def set_url(self, url):
        self.__url = url

    def load(self):
        try:
            data = requests.get(self.__url)
            self.text = data.content.decode("utf8")[16:]
            self.text = self.text.replace("</b>", "")
            self.text = f"Score {self.text}"
        except:
            print("Не удалось подключиться к URL текста")


    def draw(self):
        draw_text(self.text, *self.pos, 32, self.color)

def main():
    init_window(Settings.WIDTH, Settings.HEIGHT, "SHP")
    set_target_fps(Settings.FPS)
    update_tick = Settings.FPS * 2
    tick = -1
    teams = ["red", "green", "blue"]
    scores = []
    field = Field(Settings.URL + "/field")
    for i, team in enumerate(teams):
        text = Text([Settings.RIGHT_SPLIT + 20, 20 + i * 50], colors.WHITE)
        text.set_url(Settings.URL + f"/score/{team}")
        scores.append(text)
    while not window_should_close():
        tick += 1
        if tick % update_tick == 0:
            field.load()
            s = field.get_score()
            for i, score in enumerate(scores):
                score.text = f"Score {teams[i]}: {s[i+1]}"
                score.pos = [Settings.RIGHT_SPLIT + 20, 20 + i * 50]
        begin_drawing()
        clear_background(colors.BLACK)
        field.draw()
        for score in scores:
            score.draw()
        end_drawing()


if __name__ == '__main__':
    main()
