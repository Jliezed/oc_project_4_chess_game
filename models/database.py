from tinydb import TinyDB, Query


class DatabaseChessGame:
    """Class DatabaseChessGame refers to the database file linked to the program"""

    def __init__(self):
        self.database = TinyDB("database.json")
        self.players_table = self.database.table("players")
        self.tournaments_table = self.database.table("tournaments")
        self.rounds_table = self.database.table("rounds")
        self.matches_table = self.database.table("matches")
        self.player_query = Query()
        self.tournament_query = Query()
        self.round_query = Query()

    def reset_database(self, confirm_reset):
        """Delete all information in the database after asking user confirmation
        :param confirm_reset: str 'yes' or 'no'
        :return: deletion of the database
        """
        if confirm_reset == "yes":
            self.players_table.truncate()
            self.tournaments_table.truncate()
            self.database.all()
            print("***Database has been reset***")
