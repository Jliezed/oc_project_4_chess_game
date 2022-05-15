from tinydb import TinyDB, Query

database = TinyDB("database.json")
players_table = database.table("players")
tournaments_table = database.table("tournaments")


class Tournament:
    def __init__(self, players=[]):
        self.name = input("enter name of the tournament: ").title()
        self.location = input("enter location of the tournament: ").title()
        self.date = input("enter date of the tournament (DD/MM/YYYY): ")
        self.players = players
        self.rounds = 4
        self.rounds_list = "to define"
        self.time_control = input("enter time control of the tournament (bullet / blitz / coup rapide): ").title()
        self.description = input("enter description of the tournament: ")

    def save_tournament_to_database(self):
        save_tournament = input("Would you like to SAVE the tournament in the database ? Enter 'yes' or 'no': ")
        if save_tournament == "yes":
            tournament = {
                "name": self.name,
                "location": self.location,
                "date": self.date,
                "rounds": self.rounds,
                "players": self.players,
                "time control": self.time_control,
                "description": self.description
            }
            tournaments_table.insert(tournament)
            print(f"Tournament : {self.name} has been added to the database")

    def add_player(self, player):
        """Add a player to the tournament"""
        self.players.append(player)

    def remove_player(self, player):
        """Remove a player to the tournament"""
        self.players.remove(player)

    def display_players(self):
        """Display all players of the tournament"""
        for player in self.players:
            print(player)

    def rank_players(self):
        """Sort the list Players by the rank"""
        self.players.sort(key=lambda x: x.rank)

    def generate_first_round_pairs(self):
        round_1 = []
        if len(self.players) % 2 == 0:
            first_half = self.players[0:int(len(self.players)/2)]
            second_half = self.players[int(len(self.players)/2):]
            for a, b in zip(first_half, second_half):
                new_match = a.fullname + " vs " + b.fullname
                round_1.append(new_match)
            print(round_1)

    def enter_score(self):
        pass

    def calculate_score(self):
        pass


class Player:
    """Class Player"""
    def __init__(self):
        self.first_name = input("enter player first name: ").title()
        self.last_name = input("enter player last name: ").title()
        self.fullname = self.first_name + " " + self.last_name
        self.birth_date = input("enter player birth date (DD/MM/YYYY): ")
        self.gender = input("enter player gender (male/female): ")
        self.rank = int(input("enter player rank (number): "))
        self.score = "to define"

    def __repr__(self):
        return f"Player : {self.first_name} {self.last_name} - " \
               f"born in {self.birth_date} - {self.gender} - rank: {self.rank}"

    def save_player_to_database(self):
        save_player = input("Would you like to SAVE the player in the database ? Enter 'yes' or 'no': ")
        if save_player == "yes":
            player = {
                "fullname": self.fullname,
                "birth_date": self.birth_date,
                "gender": self.gender,
                "rank": self.rank,
            }
            players_table.insert(player)
            print(f"Player *{self.fullname}* has been added to the database")




class Round:
    def __init__(self, matchs=[]):
        self.matchs = matchs


class Match:
    def __init__(self, player_a, player_b):
        self.player_a = player_a
        self.player_b = player_b
        self.enter_score()

    def enter_score(self):
        player_a_score = float(input("Enter score of Player a (1-win/0-loss/0.5-match): "))
        player_b_score = float(input("Enter score of Player b (1-win/0-loss/0.5-match): "))
        match_score = [player_a_score, player_b_score]
        return match_score


class Database:
    def remove_player_to_database(self):
        player_query = Query()
        player_fullname = input("Enter player fullname to remove to the database: ").title()
        query_result = database.table("players").search(player_query.fullname == player_fullname)
        if query_result:
            players_table.remove(player_query.fullname == player_fullname)
            print("***Player has been removed***")
        else:
            print("Sorry, the fullname you enter doesn't exist in the database")

    def remove_tournament_to_database(self):
        tournament_query = Query()
        tournament_name = input("Enter tournament name to remove to the database: ").title()
        query_result = database.table("tournaments").search(tournament_query.name == tournament_name)
        if query_result:
            tournaments_table.remove(tournament_query.name == tournament_name)
            print("***Tournament has been removed***")
        else:
            print("Sorry, the name you enter doesn't exist in the database")