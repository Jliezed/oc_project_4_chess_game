from models.player import Player


class Match:
    def __init__(self, player_a: Player, player_b: Player, score_a="", score_b=""):
        self.player_a = player_a
        self.score_a = score_a
        self.player_b = player_b
        self.score_b = score_b
        self.players_match = [self.player_a, self.player_b]
        self.players_scores = self.display_players_score()

    # def __repr__(self):
    #     """ Better representation of a tournament instance"""
    #     return f"([{self.player_a.index},{self.score_a}],[{self.player_b.index},{self.score_b}])"

    def enter_score(self):
        print(f"MATCH: *{self.player_a.fullname}* VERSUS *{self.player_b.fullname}*")
        self.score_a = float(input(f"Enter score of {self.player_a.fullname} [1 for winner/0 for loser/0.5 for draw] : "))
        self.score_b = 1.0 - self.score_a
        print(f"Score of {self.player_b.fullname} is {self.score_b}")

        self.player_a.score += self.score_a
        self.player_b.score += self.score_b
        return self.score_a, self.score_b

    def display_winner(self):
        if self.score_a > self.score_b:
            print(f"{self.player_a.fullname} won the match")
        elif self.score_b > self.score_a:
            print(f"{self.player_b.fullname} won the match")
        else:
            print(f"Draw Match")

    def display_match(self):
        print(f"*{self.player_a.fullname}* VERSUS *{self.player_b.fullname}*")

    def display_players_score(self):
        self.players_scores = ([self.player_a.position, self.score_a], [self.player_b.position, self.score_b])
        return self.players_scores

