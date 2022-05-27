class ViewMainMenuTournamentTracker:
    def __init__(self):
        self.tournament_info = {}
        self.player_id = ""
        self.player_info = ""

    # ----- DONE -----
    def get_tournament_name(self, tournaments_table, tournament_query):
        """
        Ask user the name of the tournament to track
        :param tournaments_table: refers to tournaments tabs in the database
        :param tournament_query: refers to TinyDB query
        :return: tournament information from the database
        """
        in_database = ""
        while not in_database:
            tournament_selection = input("Which tournament would you like to track ?: ").title()
            query_result = tournaments_table.get(tournament_query.name == tournament_selection)
            if query_result is None:
                in_database = False
                print("Sorry, the name you enter doesn't exist in the database")
            else:
                self.tournament_info = query_result
                return query_result["name"]

    # ----- DONE -----
    def display_tracker_menu(self, tournament):
        """
        Display a menu with specific options for one tournament
        :return: print Tournament Tracker Menu
        """
        if len(tournament.players) < 8:
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
        elif len(tournament.players) == 8:
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
            for round in range(tournament.rounds):
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

    def get_player_fullname_to_add(self):
        # Ask user the fullname of the player
        player_fullname = input("Enter player fullname to add it to the tournament: ").title()
        return player_fullname

    def confirm_add_player_to_tournament(self, player_id, player_fullname):
        confirmation = input(
            f"Do you want to add {player_fullname} - ID : {player_id} to the tournament? Enter 'yes' or 'no': "
        ).lower()
        return confirmation

    def confirm_remove_player_to_tournament(self, player_id, player_fullname):
        confirmation = input(
            f"Do you want to remove {player_fullname} - ID : {player_id} to the tournament? Enter 'yes' or 'no': "
        ).lower()
        return confirmation

    def confirm_reset_players_list(self):
        confirmation = input(
            f"Do you want to reset the list of players of this tournament? Enter 'yes' or 'no': "
        ).lower()
        return confirmation

    def get_player_fullname_to_change_rank(self):
        player_fullname = input(f"Which player would you like to change the rank ? Enter his/her fullname: ").title()
        return player_fullname

    def get_player_fullname_to_remove(self):
        player_fullname = input(f"Enter player fullname to remove to the tournament: ").title()
        return player_fullname

    def back_to_tracker_menu(self):
        """ Ask user to go back to the menu """
        back_to_menu = input(
            "Would you like to GO BACK to the TOURNAMENT TRACKER MENU? Enter 'yes' or 'no': "
        ).lower()
        return back_to_menu

