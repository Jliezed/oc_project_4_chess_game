class Tournament:
    """Tournament object"""
    def __init__(self, name="", location="", date="", players=[], nb_rounds=4, rounds=[], time_control="", description=""):
        self.name = name
        self.location = location
        self.date = date
        self.players = players
        self.nb_rounds = nb_rounds
        self.rounds = rounds
        self.time_control = time_control
        self.description = description
        self.result = []

    def __repr__(self):
        """ Better representation of a tournament instance"""
        return (
            f"Tournament : {self.name} based in {self.location} - {self.date} "
            f"Players: {self.players} - nb rounds: {self.rounds} - Time control: {self.time_control}"
        )

    def save_to_database(self, tournaments_table):
        """Save tournament information to the JSON database file
        :param tournaments_table: refers to tournament table in database
        :return:
        """
        tournament = {
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "nb_rounds": self.nb_rounds,
            "players": self.players,
            "rounds": self.rounds,
            "time control": self.time_control,
            "description": self.description,
        }
        tournaments_table.insert(tournament)
        return print(f"Tournament : {self.name} has been added to the database")

    def search_by_name(self, tournament_name, tournament_table, tournament_query):
        query_result = tournament_table.get(tournament_query.name == tournament_name)
        self.name = query_result["name"]
        self.location = query_result["location"]
        self.date = query_result["date"]
        self.players = query_result["players"]
        self.nb_rounds = query_result["nb_rounds"]
        self.rounds = query_result["rounds"]
        self.time_control = query_result["time control"]
        self.description = query_result["description"]
        return query_result

    def update_tournament_players(self, players_list, tournament_name, tournaments_table, tournament_query):
        """Add a player to the tournament"""
        tournaments_table.update({"players": players_list}, tournament_query.name == tournament_name)
        return self.players

    def remove_player_to_tournament(self, player_id, tournaments_table, tournament_query):
        """Remove player to the tournament"""
        tournaments_table.remove(tournament_query.players == player_id)
        return self.players

    def save_rounds_to_database(self, round_to_save, tournament_name, tournaments_table, tournament_query):
        tournaments_table.update({"rounds": round_to_save}, tournament_query.name == tournament_name)
        return self.rounds

    def get_rounds_from_database(self, tournament_name, tournaments_table, tournament_query):
        tournament_info = tournaments_table.get(tournament_query.name == tournament_name)
        rounds_list = tournament_info["rounds"]
        return rounds_list

    def is_round_in_tournament(self, round_to_check, rounds_list):
        rounds_names_list = []
        for r in rounds_list:
            round_name = r["name"]
            rounds_names_list.append(round_name)
        if round_to_check in rounds_names_list:
            return True
        else:
            return False
