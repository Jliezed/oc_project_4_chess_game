from models import Player, Tournament, DatabaseChessGame
from views.tracker_view import ViewMainMenuTournamentTracker
from console import clear_console


class TournamentTrackerController:
    def __init__(self,):
        """Initialize with models from models and views"""
        self.view_main_menu_tracker = ViewMainMenuTournamentTracker()
        self.database = DatabaseChessGame()
        self.players_table = self.database.players_table
        self.tournaments_table = self.database.tournaments_table

    # User select 'tt' to Access to other options specific to one tournament
    # ----------------------------------------------------------------------
    def start_menu(self):
        # Ask user the name of the tournament to track
        tournament_name = self.view_main_menu_tracker.get_tournament_name(self.tournaments_table, self.database.tournament_query)

        # Retrieve tournament information
        tournament_to_track = Tournament()
        tournament_to_track.search_by_name(tournament_name, self.tournaments_table, self.database.tournament_query)

        back_to_menu = "yes"
        while back_to_menu == "yes":
            # Get user selection in tournament tracker menu
            user_action_tracker = self.view_main_menu_tracker.display_tracker_menu(tournament_to_track)

            # -------------------- PLAYER ---------------------
            # User select 'p' to Add a player to the tournament
            # -------------------------------------------------
            if user_action_tracker == "a":
                # Ask user the name of the player to add to the tournament
                player_fullname = self.view_main_menu_tracker.get_player_fullname_to_add()
                # Get ID of the player
                player_to_add = Player()
                try:
                    player_to_add.search_by_name(player_fullname, self.players_table, self.database.player_query)
                    player_id = player_to_add.get_player_index(player_to_add.fullname, self.players_table, self.database.player_query)

                    # Get Tournament players list and check if already in the list
                    players_list = tournament_to_track.players

                    if len(players_list) == 8:
                        print("Sorry, you can't add more than 8 players to a tournament. Please remove a player "
                              "if you still want to add another player.")
                    elif player_id in players_list:
                        print(f"{player_to_add.fullname} is already in the tournament.")
                    else:
                        confirmation = self.view_main_menu_tracker.confirm_add_player_to_tournament(player_id, player_to_add.fullname)
                        if confirmation == "yes":
                            players_list.append(player_id)
                            tournament_to_track.update_tournament_players(players_list, tournament_to_track.name, self.tournaments_table, self.database.tournament_query)
                            print(f"{player_to_add.fullname} has been added to the tournament")
                except TypeError:
                    print("The player name doesn't exist in the database.")

                self.view_main_menu_tracker.back_to_tracker_menu()
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
                    player.search_by_index(player_id, self.players_table)

                self.view_main_menu_tracker.back_to_tracker_menu()

            # User select 'pr' to modify player rank
            # --------------------------------------
            elif user_action_tracker == "pr":
                player_fullname = self.view_main_menu_tracker.get_player_fullname_to_change_rank()
                player_to_change_rank = Player()
                try:
                    player_to_change_rank.search_by_name(
                        player_fullname,
                        self.database.players_table,
                        self.database.player_query,
                    )

                    is_number = ""
                    new_rank = 0
                    while not is_number:
                        try:
                            new_rank = int(input(f"Enter new rank for {player_to_change_rank.fullname} : "))
                            is_number = True
                        except ValueError:
                            print("Please enter a number.")

                    player_to_change_rank.rank = new_rank
                    player_to_change_rank.modify_rank(
                        self.database.players_table,
                        self.database.player_query,
                    )
                    print(f"{player_to_change_rank.fullname} has a new rank: {player_to_change_rank.rank}")
                except TypeError:
                    print("The player name doesn't exist in the database.")

                self.view_main_menu_tracker.back_to_tracker_menu()
                clear_console()

            # User select 'pr' to remove a player from the tournament
            # -------------------------------------------------------
            elif user_action_tracker == "rp":
                player_fullname = self.view_main_menu_tracker.get_player_fullname_to_remove()

                # Get ID of the player
                player_to_remove = Player()
                try:
                    player_to_remove.search_by_name(player_fullname, self.players_table, self.database.player_query)
                    player_id = player_to_remove.get_player_index(player_to_remove.fullname, self.players_table,
                                                               self.database.player_query)

                    # Get Tournament players list and check if already in the list
                    players_list = tournament_to_track.players

                    if player_id not in players_list:
                        print(f"{player_to_remove.fullname} is not in the tournament.")
                    else:
                        confirmation = self.view_main_menu_tracker.confirm_remove_player_to_tournament(player_id,
                                                                                                    player_to_remove.fullname)
                        if confirmation == "yes":
                            players_list.remove(player_id)
                            tournament_to_track.update_tournament_players(players_list, tournament_to_track.name,
                                                                          self.tournaments_table,
                                                                          self.database.tournament_query)
                            print(f"{player_to_remove.fullname} has been removed to the tournament")
                except TypeError:
                    print("The player name doesn't exist in the database.")

                self.view_main_menu_tracker.back_to_tracker_menu()
                clear_console()

            # User select 'reset-p' to remove all players to the tournament
            # -------------------------------------------------------
            elif user_action_tracker == "reset-p":
                # Set players value to empty
                players_list = []
                # Confirm reset
                confirmation = self.view_main_menu_tracker.confirm_reset_players_list()

                if confirmation == "yes":
                    # Update the players database
                    tournament_to_track.update_tournament_players(players_list, tournament_to_track.name, self.database.tournaments_table,
                                                                  self.database.tournament_query)

            else:
                print("sorry your selection doesn't exist")
                back_to_menu = self.view_main_menu_tracker.back_to_tracker_menu()


