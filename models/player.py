class Player:
    """Player object can be added to a tournament object."""

    def __init__(self, first_name="", last_name="", birth_date="", gender="", rank=0,
                 cumul_score=0, id_database=""):
        self.first_name = first_name
        self.last_name = last_name
        self.fullname = first_name + " " + last_name
        self.birth_date = birth_date
        self.gender = gender
        self.rank = rank

        self.cumul_score = cumul_score
        self.id_database = id_database
        self.opponents = []

    def __repr__(self):
        """ Better representation of a player instance"""
        return (
            f"ID: {self.id_database} - Player : {self.fullname} - "
            f"Rank {self.rank} - Score: {self.cumul_score} - Opponents:"
            f" {self.opponents}"
        )

    # ------------------------------------------------
    # User select 'p' to Add a player to the database
    # ------------------------------------------------
    def save_to_database(self, players_table):
        """ Save player information to the JSON database file
        :param: players_table: refers to player tab in database
        :return: confirmation of player saved in the database
        """
        player = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "fullname": self.fullname,
            "birth_date": self.birth_date,
            "gender": self.gender,
            "rank": self.rank,
            "cumul_score": self.cumul_score,
            "opponents": self.opponents,
        }
        players_table.insert(player)
        return print(f"Player *{self.fullname}* has been added to the database")

    # ---------------------------------------------------
    # COMMON:
    # Sort Functions
    # 'results' to display tournament results
    # ---------------------------------------------------
    def search_by_index(self, id_database, players_table):
        """Search Player by Index in the Database
        :param id_database: refers to the index (int) in the database
        :param players_table: refers to players table in the database
        :return:
        """
        query_result = players_table.get(doc_id=id_database)
        self.first_name = query_result["first_name"]
        self.last_name = query_result["last_name"]
        self.fullname = query_result["fullname"]
        self.birth_date = query_result["birth_date"]
        self.gender = query_result["gender"]
        self.rank = query_result["rank"]
        self.id_database = id_database
        self.cumul_score = query_result["cumul_score"]
        self.opponents = query_result["opponents"]
        return query_result

    # -------------------------------------------------
    # COMMON:
    # 'a' to Add a player to the tournament
    # 'pr' to modify player rank
    # 'rp' to remove a player from the tournament
    # get_list_players_object()
    # -------------------------------------------------
    def search_by_fullname(self, player_fullname, players_table, player_query):
        """Search Player by Fullname in the Database
        :param player_fullname:
        :param players_table: refers to players table in the database
        :param player_query: refers to TinyDB Query
        :return:
        """
        query_result = players_table.get(player_query.fullname == player_fullname)
        self.first_name = query_result["first_name"]
        self.last_name = query_result["last_name"]
        self.fullname = query_result["fullname"]
        self.birth_date = query_result["birth_date"]
        self.gender = query_result["gender"]
        self.rank = query_result["rank"]
        self.cumul_score = query_result["cumul_score"]
        self.opponents = query_result["opponents"]
        return query_result

    # -------------------------------------------------
    # COMMON:
    # 'a' to Add a player to the tournament
    # 'rp' to remove a player from the tournament
    # -------------------------------------------------
    def get_player_index(self, player_fullname, players_table, player_query):
        """Get the ID of a player by his/her fullname
        :param player_fullname: str
        :param players_table: refers to players table in the database
        :param player_query: refers to TinyDB Query
        :return: the index in the database of the player
        """
        player_id = players_table.get(player_query.fullname == player_fullname).doc_id
        self.id_database = player_id
        return player_id

    # --------------------------------------
    # User select 'pr' to modify player rank
    # --------------------------------------
    def modify_rank(self, players_table, player_query):
        """Modify the Rank of a Player
        :param players_table: refers to players table in the database
        :param player_query: refers to TinyDB Query
        :return: the new rank of the player
        """
        players_table.update(
            {"rank": self.rank}, player_query.fullname == self.fullname
        )
        return self.rank

    # -------------------------------------------------------
    # User select 'record' to start recording matches results
    # -------------------------------------------------------
    def update_player_score_opponents(self, players_table, player_query):
        players_table.update(
            {"cumul_score": self.cumul_score}, player_query.fullname == self.fullname
        )
        players_table.update(
            {"opponents": self.opponents}, player_query.fullname == self.fullname
        )

    def update_player_rank_score_opponents(self, players_table, player_query):
        players_table.update(
            {"rank": self.rank}, player_query.fullname == self.fullname
        )
        players_table.update(
            {"cumul_score": self.cumul_score}, player_query.fullname == self.fullname
        )
        players_table.update(
            {"opponents": self.opponents}, player_query.fullname == self.fullname
        )





    def reset_score_opponents(self, players_table, player_query):
        players_table.update({"cumul_score": 0}, player_query.fullname == self.fullname)
        players_table.update({"opponents": []}, player_query.fullname == self.fullname)

    def player_details_to_dict(self):
        player_dict = {
            "id_database": self.id_database,
            "fullname": self.fullname,
            "rank": self.rank,
            "cumul_score": self.cumul_score,
            "opponents": self.opponents,
        }
        return player_dict

