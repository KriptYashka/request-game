import json

COLORS = {
    "unknown": 0,
    "red": 1,
    "green": 2,
    "blue": 3
}

class Team:
    def __init__(self, name: str):
        self.name = name.upper()
        self.score = 0
        self.solved_id = set()

    def solve(self, qid: int) -> bool:
        if qid in self.solved_id:
            return -1
        self.solved_id.add(qid)
        # TODO: добавить очки
        return 1


class Field:
    def __init__(self, n=20, m=20):
        self.field = [[0] * m for _ in range(n)]

    def set_pos(self, x, y, team: Team):
        color = COLORS[team.name]
        self.field[y][x] = color

class Questions:
    def __init__(self):
        with open("quests.json", encoding="UTF-8") as f:
            self.data = json.load(f)

class Game:
    teams = {
        "red"  : Team("red"),
        "green": Team("green"),
        "blue" : Team("blue")
    }

    field = Field()
    questions = Questions()

    @classmethod
    def solve(cls, qid: str, team_name: str):
        team_name = team_name.lower()
        if team_name not in cls.teams:
            return -2
        return cls.teams[team_name].solve(qid)
