class Team:
    def __init__(self, name: str):
        self.name = name.upper()
        self.score = 0
        self.solved_id = set()

    def solve(self, qid: int) -> bool:
        if qid in self.solved_id:
            return False
        self.solved_id.add(qid)
        # TODO: добавить очки
        return True


class Field:
    COLORS = {
        "unknown": 0,
        "red": 1,
        "green": 2,
        "blue": 3
    }
    def __init__(self, n=20, m=20):
        self.field = [[0] * m for _ in range(n)]

    def set_pos(self, x, y, team: Team):
        color = self.COLORS[team.name]
        self.field[y][x] = color

class Questions:
    def __init__(self):
        pass

class Game:
    red   = Team("red")
    green = Team("green")
    blue  = Team("blue")
    field = Field()