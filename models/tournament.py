class Tournament:
    """Tournament object which includes all information about players, rounds,
    matches and scores"""

    def __init__(self, name="", location="", date="", nb_rounds=4,
                 time_control="", description=""):
        self.name = name
        self.location = location
        self.date = date
        self.players = []
        self.players_details = []
        self.nb_rounds = nb_rounds
        self.rounds = []
        self.time_control = time_control
        self.description = description
        self.results = []

    def __repr__(self):
        """ Better representation of a tournament instance"""
        return (
            f"Tournament : {self.name} based in {self.location} - {self.date} "
            f"Players: {self.players} - nb rounds: {self.rounds} - "
            f"Time control: {self.time_control}"
        )

    # ---------------------------------------------------
    # User select 't' to Add a tournament to the database
    # ---------------------------------------------------
    def save_to_database(self, tournaments_table):
        """Save tournament information to the JSON database file
        :param tournaments_table: refers to tournament table in database
        :return:
        """
        tournament = {
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "players": self.players,
            "players_details": self.players_details,
            "nb_rounds": self.nb_rounds,
            "rounds": self.rounds,
            "time control": self.time_control,
            "description": self.description,
            "results": self.results,
        }
        tournaments_table.insert(tournament)
        return print(f"Tournament : {self.name} has been added to the database")

    # ----------------------------------------------------------------------
    # User select 'tt' to Access to other options specific to one tournament
    # ----------------------------------------------------------------------
    def search_by_name(self, tournament_name, tournament_table, tournament_query):
        query_result = tournament_table.get(tournament_query.name == tournament_name)
        self.name = query_result["name"]
        self.location = query_result["location"]
        self.date = query_result["date"]
        self.players = query_result["players"]
        self.players_details = query_result["players_details"]
        self.nb_rounds = query_result["nb_rounds"]
        self.rounds = query_result["rounds"]
        self.time_control = query_result["time control"]
        self.description = query_result["description"]
        self.results = query_result["results"]
        return query_result

    # -------------------------------------------------
    # COMMON :
    # 'a' to Add a player to the tournament
    # 'rp' to remove a player from the tournament
    # 'reset-p' to remove all players to the tournament
    # -------------------------------------------------
    def update_tournament_players(
        self, players_list, tournament_name, tournaments_table, tournament_query
    ):
        """Add a player to the tournament"""
        tournaments_table.update(
            {"players": players_list}, tournament_query.name == tournament_name
        )
        return self.players



    # -------------------------------------------------------
    # COMMON:
    # User select 'reset-p' to remove all players to the tournament
    # -------------------------------------------------------
    def update_player_details_database(self, players_details, tournament_name,
                                       tournaments_table, tournament_query):
        tournaments_table.update({"players_details": players_details},
                                 tournament_query.name == tournament_name)
        return self.players_details

    def update_rounds_database(
        self, round_to_save, tournament_name, tournaments_table, tournament_query
    ):
        tournaments_table.update(
            {"rounds": round_to_save}, tournament_query.name == tournament_name
        )
        return self.rounds

    # -------------------------------------------------------
    # User select 'record' to start recording matches results
    # -------------------------------------------------------
    def is_round_in_tournament(self, round_to_check, rounds_list):
        rounds_names_list = []
        for r in rounds_list:
            round_name = r["name"]
            rounds_names_list.append(round_name)
        if round_to_check in rounds_names_list:
            return True
        else:
            return False

    # ---------------------------------------------------
    # COMMON :
    # 'record' to start recording matches results
    # 'results' to display tournament results
    # ---------------------------------------------------
    def get_rounds_from_database(self, tournament_name, tournaments_table, tournament_query):
        tournament_info = tournaments_table.get(
            tournament_query.name == tournament_name
        )
        rounds_list = tournament_info["rounds"]
        return rounds_list

    def get_players_details_from_database(self, tournament_name, tournaments_table,
                                          tournament_query):
        tournament_info = tournaments_table.get(
            tournament_query.name == tournament_name
        )
        players_details = tournament_info["players_details"]
        return players_details

    # --------------------------------------------------------
    # User select 'dr' to display all rounds of the tournament
    # --------------------------------------------------------
    def display_rounds(self, tournament_name, tournaments_table, tournament_query):
        tournament_info = tournaments_table.get(tournament_query.name == tournament_name)
        rounds_list = tournament_info["rounds"]
        for round in rounds_list:
            round_name = round["name"]
            print(round_name, round)

    # ---------------------------------------------------------
    # User select 'dm' to display all matches of the tournament
    # ---------------------------------------------------------
    def display_matches(self, tournament_name, tournaments_table, tournament_query):
        tournament_info = tournaments_table.get(tournament_query.name == tournament_name)
        rounds_list = tournament_info["rounds"]
        for round in rounds_list:
            round_name = round["name"]
            matches = round["matches"]
            print(round_name, matches)
