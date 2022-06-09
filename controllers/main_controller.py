from models.player import Player
from models.tournament import Tournament
from models.database import DatabaseChessGame
from views.main_view import ViewMainMenu, ViewMainMenuPlayer, ViewMainMenuTournament
from controllers.tracker_controller import TournamentTrackerController
from models.console import clear_console


class MainController:
    """Controller class that run the program"""

    def __init__(self):
        """Initialize with models from models and views"""
        self.view_main_menu = ViewMainMenu()
        self.view_main_menu_player = ViewMainMenuPlayer()
        self.view_main_menu_tournament = ViewMainMenuTournament()
        self.database = DatabaseChessGame()
        self.tournaments_table = self.database.tournaments_table
        self.players_table = self.database.players_table
        self.tournament_query = self.database.tournament_query
        self.player_query = self.database.player_query
        self.user_action = ""

    def get_user_action(self):
        """ Get user selection in the menu """
        self.user_action = input("What is you selection ?: ").lower()

    def get_list_players_object(self):
        players_fullname_list = [player["fullname"] for player in self.players_table]
        players_object_list = []
        for player_fullname in players_fullname_list:
            player = Player()
            player.search_by_fullname(
                player_fullname, self.players_table, self.player_query
            )
            players_object_list.append(player)
        return players_object_list

    def start_program(self):
        back_to_menu = "yes"
        while back_to_menu == "yes":
            self.view_main_menu.show_logo()
            self.view_main_menu.display_menu()
            self.get_user_action()

            # ------------------------------------------------
            # ------------------------------------------------
            # --------------------- PLAYER -------------------
            # ------------------------------------------------
            # ------------------------------------------------

            # ------------------------------------------------
            # User select 'p' to Add a player to the database
            # ------------------------------------------------
            if self.user_action == "p":
                # Ask for player information
                player_info = self.view_main_menu_player.get_player_info()

                # Create a player instance
                new_player = Player(
                    first_name=player_info["first_name"],
                    last_name=player_info["last_name"],
                    birth_date=player_info["birth_date"],
                    gender=player_info["gender"],
                    rank=player_info["rank"],
                )

                # Ask user for confirmation to save player to the database
                should_save_player = self.view_main_menu_player.should_save_player()

                # Save player information to the database
                if should_save_player == "yes":
                    new_player.save_to_database(self.players_table)

                # Ask to go back to the main menu
                self.view_main_menu_player.back_to_menu()
                clear_console()

            # -------------------------------------------------------------
            # User select 'pla' to Display list of all players by Alphabet
            # -------------------------------------------------------------
            elif self.user_action == "pla":
                # Sort Players by alphabet
                players_sorted_by_alphabet = self.get_list_players_object()
                players_sorted_by_alphabet.sort(key=lambda player: player.fullname)
                # Display All Players by Alphabet
                self.view_main_menu_player.display_all_players(
                    players_sorted_by_alphabet
                )

                # Ask to go back to the main menu
                self.view_main_menu_player.back_to_menu()
                clear_console()

            # ---------------------------------------------------------
            # User select 'plr' to Display list of all players by Rank
            # ---------------------------------------------------------
            elif self.user_action == "plr":
                # Sort Players by Rank
                players_sorted_by_rank = self.get_list_players_object()
                players_sorted_by_rank.sort(key=lambda player: player.rank)
                # Display All Players by Rank
                self.view_main_menu_player.display_all_players(players_sorted_by_rank)

                # Ask to go back to the main menu
                self.view_main_menu_player.back_to_menu()
                clear_console()

            # ----------------------------------------------
            # User select 'pi' to Display player information
            # ----------------------------------------------
            elif self.user_action == "pi":
                # Display player information for a specific player from user entry
                self.view_main_menu_player.display_player_information(
                    self.players_table, self.player_query,
                )

                # Ask to go back to the main menu
                self.view_main_menu_player.back_to_menu()
                clear_console()

            # ---------------------------------------------------
            # ---------------------------------------------------
            # ------------------- TOURNAMENT --------------------
            # ---------------------------------------------------
            # ---------------------------------------------------

            # ---------------------------------------------------
            # User select 't' to Add a tournament to the database
            # ---------------------------------------------------
            elif self.user_action == "t":
                # Add a tournament to the database
                tournament_info = self.view_main_menu_tournament.get_tournament_info()

                # Create a tournament instance
                new_tournament = Tournament(
                    name=tournament_info["name"],
                    location=tournament_info["location"],
                    date=tournament_info["date"],
                    time_control=tournament_info["time_control"],
                    description=tournament_info["description"],
                )

                # Ask user for confirmation to save tournament to the database
                should_save_tournament = (
                    self.view_main_menu_tournament.should_save_tournament()
                )

                # Save tournament information to the database
                if should_save_tournament == "yes":
                    new_tournament.save_to_database(self.tournaments_table)

                # Ask to go back to the main menu
                self.view_main_menu_tournament.back_to_menu()
                clear_console()

            # ---------------------------------------------------
            # User select 'tl' to Display list of all tournaments
            # ---------------------------------------------------
            elif self.user_action == "tl":
                # Display all tournaments saved in the database
                self.view_main_menu_tournament.display_all_tournaments(
                    self.tournaments_table
                )

                # Ask to go back to the main menu
                self.view_main_menu_tournament.back_to_menu()
                clear_console()

            # --------------------------------------------------
            # User select 'ti' to Display tournament information
            # --------------------------------------------------
            elif self.user_action == "ti":
                # Display tournament information
                self.view_main_menu_tournament.display_tournament_information(
                    self.tournaments_table, self.tournament_query,
                )

                # Ask to go back to the main menu
                self.view_main_menu_tournament.back_to_menu()
                clear_console()

            # -------------------------------------------------------------
            # -------------------------------------------------------------
            # --------------------------- RESET ---------------------------
            # -------------------------------------------------------------
            # -------------------------------------------------------------

            # -------------------------------------------------------------
            # User select 'reset' to delete all information in the database
            # -------------------------------------------------------------
            elif self.user_action == "reset":
                confirm_reset = self.view_main_menu.confirm_reset()
                self.database.reset_database(confirm_reset)

                # Ask to go back to the main menu
                self.view_main_menu.back_to_menu()
                clear_console()

            # -------------------------------------------------------------
            # -------------------------------------------------------------
            # --------------------- TOURNAMENT TRACKER --------------------
            # -------------------------------------------------------------
            # -------------------------------------------------------------
            elif self.user_action == "tt":
                clear_console()
                tournament_tracker_menu = TournamentTrackerController()
                tournament_tracker_menu.start_menu()

            # -------------------------------------------------------------
            # User select 'q' to quit
            # -------------------------------------------------------------
            elif self.user_action == "q":
                exit()

            else:
                # Ask to go back to the main menu
                self.view_main_menu.back_to_menu()
                clear_console()
