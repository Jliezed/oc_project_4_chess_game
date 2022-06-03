class Player:
    """Player object can be added to a tournament object."""
    def __init__(self, first_name="", last_name="", birth_date="", gender="", rank=0, score=0, position=""):
        self.first_name = first_name
        self.last_name = last_name
        self.fullname = first_name + " " + last_name
        self.birth_date = birth_date
        self.gender = gender
        self.rank = rank
        self.score = score
        self.position = position

    # def __repr__(self):
    #     """ Better representation of a player instance"""
    #     return (
    #         f"ID: {self.position} - Player : {self.fullname} - "
    #         f"born in {self.birth_date} - {self.gender} - rank: {self.rank}"
    #     )


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
            "current_score": self.score,
        }
        players_table.insert(player)
        return print(f"Player *{self.fullname}* has been added to the database")

    def search_by_index(self, index_player, players_table):
        """Search Player by Index in the Database
        :param index_player: refers to the index (int) in the database
        :param players_table: refers to players table in the database
        :return:
        """
        query_result = players_table.get(doc_id=index_player)
        self.first_name = query_result["first_name"]
        self.last_name = query_result["last_name"]
        self.fullname = query_result["fullname"]
        self.birth_date = query_result["birth_date"]
        self.gender = query_result["gender"]
        self.rank = query_result["rank"]
        self.position = index_player
        return query_result

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
        return query_result

    def get_player_index(self, player_fullname, players_table, player_query):
        """Get the ID of a player by his/her fullname
        :param player_fullname: str
        :param players_table: refers to players table in the database
        :param player_query: refers to TinyDB Query
        :return: the index in the database of the player
        """
        player_id = players_table.get(player_query.fullname == player_fullname).doc_id
        self.position = player_id
        return player_id

    def modify_rank(self, players_table, player_query):
        """Modify the Rank of a Player
        :param players_table: refers to the players table in the database
        :param player_query: refers to TinyDB Query
        :return: the new rank of the player
        """
        players_table.update({"rank": self.rank}, player_query.fullname == self.fullname)
        return self.rank
