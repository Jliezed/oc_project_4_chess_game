class Controller:
    """
    Controller class that run the program
    ...
    Attributes
    ----------
    view_main_menu: refers to the class ViewMainMenu
    view_main_menu_player: refers to the class ViewMainMenuPlayer
    view_main_menu_tournament: refers to the class ViewMainMenuTournament
    view_main_menu_tournament_tracker: refers to the class ViewMainMenuTournamentTracker
    database_chess_game: refers to the class DatabaseChessGame
    player: refers to Player class
    tournament: refers to Tournament class

    Methods
    ----------



    """

    def __init__(
        self,
        view_main_menu,
        view_main_menu_player,
        view_main_menu_tournament,
        view_main_menu_tournament_tracker,
        database_chess_game,
        player,
        tournament,
    ):
        """Initialize with models from models and views"""
        self.view_main_menu = view_main_menu
        self.view_main_menu_player = view_main_menu_player
        self.view_main_menu_tournament = view_main_menu_tournament
        self.view_main_menu_tournament_tracker = view_main_menu_tournament_tracker
        self.database_chess_game = database_chess_game

        self.user_action = ""

        self.player = player
        self.tournament = tournament

    def get_user_action(self):
        """ Get user selection in the menu """
        self.user_action = input("What is you selection ?: ").lower()

    def start_program(self):
        back_to_menu = "yes"
        while back_to_menu == "yes":
            self.view_main_menu.display_menu()
            self.get_user_action()

            # ------------------------------------------------
            # ------------------------------------------------
            # --------------------- PLAYER -------------------
            # ------------------------------------------------
            # ------------------------------------------------

            # User select 'p' to Add a player to the database
            # ------------------------------------------------
            if self.user_action == "p":
                # Ask for player information
                player_info = self.view_main_menu_player.get_player_info()

                # Feed Player class object
                self.player.first_name = player_info["first_name"]
                self.player.last_name = player_info["last_name"]
                self.player.fullname = (
                    self.player.first_name + " " + self.player.last_name
                )
                self.player.birth_date = player_info["birth_date"]
                self.player.gender = player_info["gender"]
                self.player.rank = player_info["rank"]

                # Ask user for confirmation to save player to the database
                should_save_player = self.view_main_menu_player.should_save_player()

                # Save player information to the database
                self.player.save_to_database(
                    should_save_player, self.database_chess_game.players_table
                )

                # Ask to go back to the main menu
                self.view_main_menu_player.back_to_menu()

            # User select 'pl' to Display list of all players
            # -----------------------------------------------
            elif self.user_action == "pl":
                # Display all players saved in the database
                self.view_main_menu_player.display_all_players(
                    self.database_chess_game.players_table
                )

                # Ask to go back to the main menu
                self.view_main_menu_player.back_to_menu()

            # User select 'pi' to Display player information
            # ----------------------------------------------
            elif self.user_action == "pi":
                # Display player information for a specific player from user entry
                self.view_main_menu_player.display_player_information(
                    self.database_chess_game.players_table,
                    self.database_chess_game.player_query,
                )

                # Ask to go back to the main menu
                self.view_main_menu_player.back_to_menu()

            # ---------------------------------------------------
            # ---------------------------------------------------
            # ------------------- TOURNAMENT --------------------
            # ---------------------------------------------------
            # ---------------------------------------------------

            # User select 't' to Add a tournament to the database
            # ---------------------------------------------------
            elif self.user_action == "t":
                # Add a tournament to the database
                tournament_info = self.view_main_menu_tournament.get_tournament_info()

                # Feed Tournament class object
                self.tournament.name = tournament_info["name"]
                self.tournament.location = tournament_info["location"]
                self.tournament.date = tournament_info["date"]
                self.tournament.time_control = tournament_info["time_control"]
                self.tournament.description = tournament_info["description"]

                # Ask user for confirmation to save tournament to the database
                should_save_tournament = (
                    self.view_main_menu_tournament.should_save_tournament()
                )

                # Save tournament information to the database
                self.tournament.save_to_database(
                    should_save_tournament, self.database_chess_game.tournaments_table
                )

                # Ask to go back to the main menu
                self.view_main_menu_tournament.back_to_menu()

            # User select 'tl' to Display list of all tournaments
            # ---------------------------------------------------
            elif self.user_action == "tl":
                # Display all tournaments saved in the database
                self.view_main_menu_tournament.display_all_tournaments(
                    self.database_chess_game.tournaments_table
                )

                # Ask to go back to the main menu
                self.view_main_menu_tournament.back_to_menu()

            # User select 'ti' to Display tournament information
            # --------------------------------------------------
            elif self.user_action == "ti":
                # Display tournament information
                self.view_main_menu_tournament.display_tournament_information(
                    self.database_chess_game.tournaments_table,
                    self.database_chess_game.tournament_query,
                )

                # Ask to go back to the main menu
                self.view_main_menu_tournament.back_to_menu()

            # -----------------------------------------------------------------------
            # -----------------------------------------------------------------------
            # --------------------------- TOURNAMENT TRACKER ------------------------
            # -----------------------------------------------------------------------
            # -----------------------------------------------------------------------

            # User select 'tt' to Access to other options specific to one tournament
            # -----------------------------------------------------------------------
            elif self.user_action == "tt":
                # Ask user the name of the tournament to track
                self.view_main_menu_tournament_tracker.get_tournament_name(
                    self.database_chess_game.tournaments_table,
                    self.database_chess_game.tournament_query,
                )
                # Add the name of the tournament to the tournament object
                self.tournament.name = self.view_main_menu_tournament_tracker.tournament_info["name"]

                # Get user selection in tournament tracker menu
                user_action_tracker = (
                    self.view_main_menu_tournament_tracker.display_tournament_tracker_menu()
                )

                # -------------------- PLAYER ---------------------
                # User select 'p' to Add a player to the tournament
                # -------------------------------------------------
                if user_action_tracker == "p":
                    # Ask user the name of the player to add to the tournament
                    self.view_main_menu_tournament_tracker.get_player_to_add_to_tournament(
                        self.database_chess_game.players_table,
                        self.database_chess_game.player_query,
                    )

                    # Add the player to the tournament
                    self.tournament.players = self.view_main_menu_tournament_tracker.tournament_info["players"]
                    self.tournament.add_player_to_tournament(self.database_chess_game.tournaments_table, self.database_chess_game.tournament_query)


                # User select 'pl' to display the list of all players in the tournament
                # -------------------------------------------------

                elif user_action_tracker == "pl":
                    # Display list of players of the tournament
                    pass
                elif user_action_tracker == "pl":
                    pass
                elif user_action_tracker == "pr":
                    pass
                elif user_action_tracker == "xx":
                    pass
                else:
                    print("sorry your selection doesn't exist")
                self.view_main_menu_tournament_tracker.back_to_tracker_menu()

            # ---------------------------- RESET --------------------------
            # User select 'reset' to delete all information in the database
            elif self.user_action == "reset":
                confirm_reset = self.view_main_menu.confirm_reset()
                self.database_chess_game.reset_database(confirm_reset)

                # Ask to go back to the main menu
                self.view_main_menu.back_to_menu()
            else:
                # Ask to go back to the main menu
                self.view_main_menu.back_to_menu()
