class ViewMainMenuTournamentTracker:
    def __init__(self):
        self.tournament_info = {}
        self.player_id = ""
        self.player_info = ""

    def get_tournament_name(self, tournaments_table, tournament_query):
        """
        Ask user the name of the tournament to track
        :param tournaments_table: refers to tournaments tabs in the database
        :param tournament_query: refers to TinyDB query
        :return: tournament information from the database
        """
        in_database = ""
        while not in_database:
            tournament_selection = input(
                "Which tournament would you like to track ?: "
            ).title()
            query_result = tournaments_table.get(
                tournament_query.name == tournament_selection
            )
            if query_result is None:
                in_database = False
                print("Sorry, the name you enter doesn't exist in the database")
            else:
                self.tournament_info = query_result
                return query_result["name"]

    def display_tournament_tracker_menu(self):
        """
        Display a menu with specific options for one tournament
        :return: print Tournament Tracker Menu
        """
        if len(self.tournament_info["players"]) < 8:
            print(
                "-----------------------------------------------------------\n"
                "------------- WELCOME TO TOURNAMENT TRACKER ----------------\n"
                "-----------------------------------------------------------\n"
                "------------------------ PLAYERS ---------------------------\n"
                "enter 'a' : Add a player to the tournament\n"
                "enter 'lp' : Display list of players\n"
                "enter 'pr' : Modify the rank of a player\n"
                "enter 'rp' : Remove a player to the tournament\n"
                "-----------------------------------------------------------\n"
                "*Add 8 players to the tournament to start the score tracker*\n"
                "-----------------------------------------------------------\n"
            )
        elif len(self.tournament_info["players"]) == 8:
            print(
                "-------------------------------------------------------\n"
                "------------ WELCOME TO TOURNAMENT TRACKER ------------\n"
                "-------------------------------------------------------\n"
                "------------------------ PLAYERS ----------------------\n"
                "enter 'lp' : Display list of players\n"
                "enter 'pr' : Modify the rank of a player\n"
                "enter 'reset-p' : Reset players to this tournament\n"
                "-------------------------------------------------------"
            )
            print("--------------------- ROUNDS --------------------")
            for round in range(self.tournament_info["rounds"]):
                round += 1
                print(
                    f"enter 'r{round}' : Display Round {round}\n"
                    f"enter 'sr{round}' : Enter score of Round {round}"
                )
            print(
                "------------------- GET RESULTS ------------------\n"
                "enter 'results' : Get results of the tournament\n"
                "--------------------- REPORTS --------------------\n"
                "enter 'r' : TO DEFINE\n"
                "enter 'r' : TO DEFINE\n"
                "--------------------------------------------------\n"
                "Press 'q' to QUIT"
            )
        user_action = input("What is you selection ?: ")
        return user_action

    def get_player_to_add_to_tournament(self, players_table, player_query):
        """
        Ask user the fullname of the player to add to the tournament

        """
        # Ask user the fullname of the player
        fullname = input("Enter player fullname to add it to the tournament: ").title()
        # Retrieve user ID in the database
        player_id = players_table.get(player_query.fullname == fullname).doc_id
        # Feed self variable
        self.tournament_info["players"].append(player_id)
        self.player_id = player_id
        player_info = players_table.get(player_query.fullname == fullname)
        self.player_info = player_info

    def confirm_add_player_to_tournament(self):
        confirmation = input(
            f"Do you want to add {self.player_info['fullname']} - ID : {self.player_id} to the tournament? Enter 'yes' or 'no': "
        ).lower()
        return confirmation

    def get_player_to_remove(self):
        player_fullname = input(
            f"Enter the player fullname to remove to the tournament: "
        ).title()
        return player_fullname

    def back_to_tracker_menu(self):
        """ Ask user to go back to the menu """
        back_to_menu = input(
            "Would you like to GO BACK to the TOURNAMENT TRACKER MENU? Enter 'yes' or 'no': "
        ).lower()
        return back_to_menu
