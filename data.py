import json
from typing import Optional

COLORS = {
    "unknown": 0,
    "red": 1,
    "green": 2,
    "blue": 3
}

class Team:
    def __init__(self):
        self.score = 0
        self.solved_id = set()

    def solve(self, qid: str, score: int) -> int:
        if qid in self.solved_id:
            return -1
        self.solved_id.add(qid)
        self.score += score
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
        "red"  : Team(),
        "green": Team(),
        "blue" : Team()
    }

    field = Field()
    questions = Questions()

    @classmethod
    def get_team(cls, team_name: str) -> Optional[Team]:
        team_name = team_name.lower()
        if team_name not in cls.teams:
            return None
        return cls.teams[team_name]


    @classmethod
    def solve(cls, qid: str, team_name: str):
        if (team := cls.get_team(team_name)) is None:
            return -2
        score = cls.questions.data[qid]["score"]
        return team.solve(qid, score)

    @classmethod
    def get_score(cls, team_name: str):
        if (team := cls.get_team(team_name)) is None:
            return -2
        return team.score
