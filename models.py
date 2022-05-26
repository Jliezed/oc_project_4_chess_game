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

    def __init__(
        self, first_name="", last_name="", birth_date="", gender="", rank=0, score=""
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.fullname = first_name + " " + last_name
        self.birth_date = birth_date
        self.gender = gender
        self.rank = rank
        self.score = score

    def __repr__(self):
        """ Better representation of a player instance"""
        return (
            f"Player : {self.fullname} - "
            f"born in {self.birth_date} - {self.gender} - rank: {self.rank}"
        )

    def save_to_database(self, players_table):
        """ Save player information to the JSON database file

        :parameter
        should_save_player: str 'yes' or 'no'
        players_table: refers to player tab in database
        """

        player = {
            "fullname": self.fullname,
            "birth_date": self.birth_date,
            "gender": self.gender,
            "rank": self.rank,
        }
        players_table.insert(player)
        print(f"Player *{self.fullname}* has been added to the database")

    def search_by_index(self, index_player, players_table):
        query_result = players_table.get(doc_id=index_player)
        self.fullname = query_result["fullname"]
        self.birth_date = query_result["birth_date"]
        self.gender = query_result["gender"]
        self.rank = query_result["rank"]
        print(
            f"Player ID: {index_player} - Fullname: {query_result['fullname']} - Gender: {query_result['gender']} - Rank: {query_result['rank']}"
        )

    def search_by_name(self, player_fullname, players_table, player_query):
        query_result = players_table.get(player_query.fullname == player_fullname)
        self.fullname = query_result["fullname"]
        self.birth_date = query_result["birth_date"]
        self.gender = query_result["gender"]
        self.rank = query_result["rank"]
        print(f"Fullname: {query_result['fullname']} - Rank: {query_result['rank']}")

    def modify_rank(self, players_table, player_query):
        players_table.update(
            {"rank": self.rank}, player_query.fullname == self.fullname
        )

    def get_player_index(self, player_fullname, players_table, player_query):
        player_id = players_table.get(player_query.fullname == player_fullname).doc_id
        return player_id


class Tournament:
    """
    Tournament object
    """

    def __init__(
        self,
        name="",
        location="",
        date="",
        players=[],
        rounds=4,
        rounds_list="blitz",
        time_control="",
        description="",
    ):
        self.name = name
        self.location = location
        self.date = date
        self.players = players
        self.rounds = rounds
        self.rounds_list = rounds_list
        self.time_control = time_control
        self.description = description

    def __repr__(self):
        """ Better representation of a tournament instance"""
        return (
            f"Tournament : {self.name} based in {self.location} - {self.date} "
            f"Players: {self.players} - rounds: {self.rounds} - Time control: {self.time_control}"
        )

    def save_to_database(self, tournaments_table):
        """
        Save tournament information to the JSON database file
        :param should_save_tournament: 'yes' or 'no'
        :param tournaments_table: refers to tournament tab in database
        :return:
        """

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

    def search_by_name(self, tournament_name, tournament_table, tournament_query):
        query_result = tournament_table.get(tournament_query.name == tournament_name)

        self.name = query_result["name"]
        self.location = query_result["location"]
        self.date = query_result["date"]
        self.players = query_result["players"]
        self.rounds = query_result["rounds"]
        # self.rounds_list = query_result["rounds_list"]
        self.time_control = query_result["time control"]
        self.description = query_result["description"]
        return query_result

    def update_tournament_players(self, tournaments_table, tournament_query):
        """Add a player to the tournament"""
        tournaments_table.update(
            {"players": self.players}, tournament_query.name == self.name
        )

    def remove_player_to_tournament(
        self, player_id, tournaments_table, tournament_query
    ):
        tournaments_table.remove(tournament_query.players == player_id)


