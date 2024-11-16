from raylib import colors
from pyray import *

import requests

class Settings:
    WIDTH, HEIGHT = 1420, 800
    FPS = 10

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
        padding = 20
        space = 2
        try:
            n, m = len(self.data[0]), len(self.data)
        except:
            return None
        size_matrix = Settings.HEIGHT - 2 * padding
        size_cell = size_matrix // min(n, m)
        for y in range(n):
            for x in range(m):
                value = self.data[y][x]
                color = self.COLORS[value]
                cell = Rectangle(padding + x * size_cell, padding + y * size_cell,
                                 size_cell - space, size_cell - space)
                draw_rectangle_rec(cell, color)




def main():
    init_window(Settings.WIDTH, Settings.HEIGHT, "SHP")
    set_target_fps(Settings.FPS)
    update_tick = Settings.FPS * 2
    tick = -1
    field = Field("http://127.0.0.1:5000/field")
    while not window_should_close():
        tick += 1
        if tick % update_tick == 0:
            field.load()
        begin_drawing()
        clear_background(colors.BLACK)
        field.draw()
        end_drawing()



if __name__ == '__main__':
    main()
