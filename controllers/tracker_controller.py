from models import Player, Tournament, DatabaseChessGame
from views.tracker_view import ViewMainMenuTournamentTracker
from console import clear_console


class TournamentTrackerController:
    def __init__(self,):
        """Initialize with models from models and views"""
        self.view_main_menu_tournament_tracker = ViewMainMenuTournamentTracker()
        self.database_chess_game = DatabaseChessGame()

    # User select 'tt' to Access to other options specific to one tournament
    # -----------------------------------------------------------------------
    def start_menu(self):
        # Ask user the name of the tournament to track
        tournament_name = self.view_main_menu_tournament_tracker.get_tournament_name(
            self.database_chess_game.tournaments_table,
            self.database_chess_game.tournament_query,
        )

        # Retrieve tournament information
        tournament_to_track = Tournament()
        tournament_to_track.search_by_name(
            tournament_name,
            self.database_chess_game.tournaments_table,
            self.database_chess_game.tournament_query,
        )

        back_to_menu = "yes"
        while back_to_menu == "yes":
            # Get user selection in tournament tracker menu
            user_action_tracker = (
                self.view_main_menu_tournament_tracker.display_tournament_tracker_menu()
            )

            # -------------------- PLAYER ---------------------
            # User select 'p' to Add a player to the tournament
            # -------------------------------------------------
            if user_action_tracker == "a":
                # Ask user the name of the player to add to the tournament
                player_id = self.view_main_menu_tournament_tracker.get_player_to_add_to_tournament(
                    self.database_chess_game.players_table,
                    self.database_chess_game.player_query,
                )
                tournament_to_track.update_tournament_players()

                # Update the value of players in the tournament
                if (
                    self.view_main_menu_tournament_tracker.player_id
                    in tournament_to_track.players
                ):
                    print("Player is already in the tournament.")
                else:
                    tournament_to_track.players = self.view_main_menu_tournament_tracker.tournament_info[
                        "players"
                    ]

                    # Get user confirmation to save the adding player to the database
                    save_to_database = (
                        self.view_main_menu_tournament_tracker.confirm_add_player_to_tournament()
                    )

                    # Update the tournament info in the database
                    if save_to_database == "yes":
                        tournament_to_track.update_tournament_players(
                            self.database_chess_game.tournaments_table,
                            self.database_chess_game.tournament_query,
                        )

                # self.view_main_menu_tournament_tracker.back_to_tracker_menu()
                clear_console()
            # User select 'pl' to display the list of all players in the tournament
            # ---------------------------------------------------------------------
            elif user_action_tracker == "lp":
                # Display list of players of the tournament
                print(
                    f"There are {len(tournament_to_track.players)} players in the tournament :\n"
                    f"----------------------------------------"
                )
                for player_id in tournament_to_track.players:
                    player = Player()
                    player.search_by_index(
                        player_id, self.database_chess_game.players_table
                    )

            # User select 'pr' to modify player rank
            # --------------------------------------
            elif user_action_tracker == "pr":
                player_fullname = input(
                    f"Which player would you like to change the rank ? Enter his/her fullname: "
                ).title()
                player = Player()
                try:
                    player.search_by_name(
                        player_fullname,
                        self.database_chess_game.players_table,
                        self.database_chess_game.player_query,
                    )
                except TypeError:
                    print("The player name doesn't exist in the database.")

                is_number = ""
                new_rank = 0
                while not is_number:
                    try:
                        new_rank = int(input("New Rank: "))
                        is_number = True
                    except ValueError:
                        print("Please enter a number.")

                player.rank = new_rank
                player.modify_rank(
                    self.database_chess_game.players_table,
                    self.database_chess_game.player_query,
                )

                self.view_main_menu_tournament_tracker.back_to_tracker_menu()
                clear_console()

            # User select 'pr' to remove a player from the tournament
            # -------------------------------------------------------
            elif user_action_tracker == "rp":
                player_fullname = (
                    self.view_main_menu_tournament_tracker.get_player_to_remove()
                )
                player = Player()
                player.search_by_name(
                    player_fullname,
                    self.database_chess_game.players_table,
                    self.database_chess_game.player_query,
                )
                player_index = player.get_player_index(
                    player_fullname,
                    self.database_chess_game.players_table,
                    self.database_chess_game.player_query,
                )
                tournament_to_track.players.remove(player_index)
                tournament_to_track.update_tournament_players(
                    self.database_chess_game.tournaments_table,
                    self.database_chess_game.tournament_query,
                )

                self.view_main_menu_tournament_tracker.back_to_tracker_menu()
                clear_console()

            # User select 'reset-p' to remove all players to the tournament
            # -------------------------------------------------------
            elif user_action_tracker == "reset-p":
                # Set players value to empty
                tournament_to_track.players = []
                # Update the players database
                tournament_to_track.update_tournament_players(self.database_chess_game.tournaments_table,
                    self.database_chess_game.tournament_query,)

            else:
                print("sorry your selection doesn't exist")
            back_to_menu = self.view_main_menu_tournament_tracker.back_to_tracker_menu()
