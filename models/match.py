class Match:
    """Match Class used when Round start"""
    def __init__(self, player_a, player_b, score_a="", score_b=""):
        self.player_a = player_a
        self.score_a = score_a
        self.player_b = player_b
        self.score_b = score_b
        self.players_match = [self.player_a, self.player_b]
        self.players_scores = self.display_players_score()

    # def __repr__(self):
    #     """ Better representation of a tournament instance"""
    #     return f"([{self.player_a.index},{self.score_a}],[{self.player_b.index},{self.score_b}])"

    # --------------------------
    # Function get_score_round()
    # --------------------------
    def enter_score(self):
        """Ask user to enter score for a match"""
        print(f"MATCH: *{self.player_a.fullname}* VERSUS *{self.player_b.fullname}*")
        # Score enter by user need to match 0 or 1 or 0.5
        is_score = ""
        while not is_score:
            self.score_a = float(
                input(
                    f"Enter score of {self.player_a.fullname} [1 for winner/0 for loser/0.5 for draw] : "
                )
            )
            if self.score_a == 0 or self.score_a == 1 or self.score_a == 0.5:
                is_score = True
            else:
                is_score = False
        # Score of player B is automatically calculated
        self.score_b = 1.0 - self.score_a
        print(f"Score of {self.player_b.fullname} is {self.score_b}")

        # Increment scores for each player
        self.player_a.cumul_score += self.score_a
        self.player_b.cumul_score += self.score_b
        return self.score_a, self.score_b

    def display_winner(self):
        if self.score_a > self.score_b:
            print(f"{self.player_a.fullname} won the match")
        elif self.score_b > self.score_a:
            print(f"{self.player_b.fullname} won the match")
        else:
            print("Draw Match")

    def display_players_score(self):
        self.players_scores = (
            [self.player_a.id_database, self.score_a],
            [self.player_b.id_database, self.score_b],
        )
        return self.players_scores

    # --------------------------------------
    # Function generate_next_round_matches()
    # --------------------------------------
    def display_match(self):
        print(f"*{self.player_a.fullname}* VERSUS *{self.player_b.fullname}*")
