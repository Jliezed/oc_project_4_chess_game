from tinydb import TinyDB, Query


class DatabaseChessGame:
    """Class DatabaseChessGame refers to the database file linked to the program"""
    def __init__(self):
        self.database = TinyDB("database.json")
        self.players_table = self.database.table("players")
        self.tournaments_table = self.database.table("tournaments")
        self.player_query = Query()
        self.tournament_query = Query()

    def reset_database(self, confirm_reset):
        """
        Delete all information in the database after asking user confirmation
        :param confirm_reset: str 'yes' or 'no'
        :return: deletion of the database
        """
        if confirm_reset == "yes":
            self.players_table.truncate()
            self.tournaments_table.truncate()
            self.database.all()
            print("***Database has been reset***")


class Player:
    """
    Player object can be added to a tournament object.
    """

    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.fullname = ""
        self.birth_date = ""
        self.gender = ""
        self.rank = 0
        self.score = ""

    def __repr__(self):
        """ Better representation of a player instance"""
        return (
            f"Player : {self.first_name} {self.last_name} - "
            f"born in {self.birth_date} - {self.gender} - rank: {self.rank}"
        )

    def save_to_database(self, should_save_player, players_table):
        """ Save player information to the JSON database file

        :parameter
        should_save_player: str 'yes' or 'no'
        players_table: refers to player tab in database
        """

        if should_save_player == "yes":
            player = {
                "fullname": self.fullname,
                "birth_date": self.birth_date,
                "gender": self.gender,
                "rank": self.rank,
            }
            players_table.insert(player)
            print(f"Player *{self.fullname}* has been added to the database")


class Tournament:
    """
    Tournament object
    """
    def __init__(self):
        self.name = ""
        self.location = ""
        self.date = ""
        self.players = []
        self.rounds = 4
        self.rounds_list = "to define"
        self.time_control = ""
        self.description = ""

    def __repr__(self):
        """ Better representation of a tournament instance"""
        return (
            f"Tournament : {self.name} based in {self.location} - {self.date} "
            f"Players: {self.players} - rounds: {self.rounds} - Time control: {self.time_control}"
        )

    def save_to_database(self, should_save_tournament, tournaments_table):
        """
        Save tournament information to the JSON database file
        :param should_save_tournament: 'yes' or 'no'
        :param tournaments_table: refers to tournament tab in database
        :return:
        """
        if should_save_tournament == "yes":
            tournament = {
                "name": self.name,
                "location": self.location,
                "date": self.date,
                "rounds": self.rounds,
                "players": self.players,
                "time control": self.time_control,
                "description": self.description,
            }
            tournaments_table.insert(tournament)
            print(f"Tournament : {self.name} has been added to the database")

    def add_player_to_tournament(self, tournaments_table, tournament_query):
        """Add a player to the tournament"""
        tournaments_table.update({"players": self.players}, tournament_query.name == self.name)


