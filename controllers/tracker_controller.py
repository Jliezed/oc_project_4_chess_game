from models.round import Round
from models.match import Match
from models.tournament import Tournament
from models.database import DatabaseChessGame
from models.player import Player
from views.tracker_view import ViewMainMenuTournamentTracker
from models.console import clear_console


class TournamentTrackerController:
    def __init__(self,):
        """Initialize with models from models and views"""
        self.view_main_menu_tracker = ViewMainMenuTournamentTracker()
        self.database = DatabaseChessGame()
        self.players_table = self.database.players_table
        self.tournaments_table = self.database.tournaments_table
        self.rounds_table = self.database.rounds_table
        self.matches_table = self.database.matches_table
        self.tournament_to_track = Tournament()

    def get_list_players_object(self):
        list_players = self.tournament_to_track.players
        players_object_list = []
        for player_id in list_players:
            player_to_sort = Player()
            player_to_sort.search_by_index(player_id, self.players_table)
            players_object_list.append(player_to_sort)
        return players_object_list

    def generate_first_round(self, players_in_tournament):
        players_in_tournament.sort(key=lambda player: player.rank)
        first_set = players_in_tournament[:4]
        second_set = players_in_tournament[4:]
        matches_first_round = []
        for player_first_set, player_second_set in zip(first_set, second_set):
            match = Match(player_first_set, player_second_set)
            match.display_match()
            matches_first_round.append(match)
        return matches_first_round

    def enter_score_first_round(self, matches_first_round):
        matches_recorded = []
        for match in matches_first_round:
            match.enter_score()
            match.display_winner()
            match.display_players_score()
            matches_recorded.append(match.players_scores)
        print(type(matches_recorded))
        return matches_recorded

    # User select 'tt' to Access to other options specific to one tournament
    # ----------------------------------------------------------------------
    def start_menu(self):
        # Ask user the name of the tournament to track
        tournament_name = self.view_main_menu_tracker.get_tournament_name(
            self.tournaments_table, self.database.tournament_query
        )

        # Retrieve tournament information
        self.tournament_to_track.search_by_name(
            tournament_name, self.tournaments_table, self.database.tournament_query
        )

        back_to_menu = "yes"
        while back_to_menu == "yes":
            # Get user selection in tournament tracker menu
            user_action_tracker = self.view_main_menu_tracker.display_tracker_menu(
                self.tournament_to_track
            )

            # -------------------- PLAYER ---------------------
            # -------------------------------------------------
            # User select 'a' to Add a player to the tournament
            # -------------------------------------------------
            if user_action_tracker == "a":
                # Ask user the name of the player to add to the tournament
                player_fullname = (
                    self.view_main_menu_tracker.get_player_fullname_to_add()
                )
                # Get ID of the player
                player_to_add = Player()
                try:
                    player_to_add.search_by_fullname(
                        player_fullname, self.players_table, self.database.player_query
                    )
                    player_id = player_to_add.get_player_index(
                        player_to_add.fullname,
                        self.players_table,
                        self.database.player_query,
                    )

                    # Get Tournament players list and check if already in the list
                    players_list = self.tournament_to_track.players

                    if len(players_list) == 8:
                        print(
                            "Sorry, you can't add more than 8 players to a tournament. Please remove a player "
                            "if you still want to add another player."
                        )
                    elif player_id in players_list:
                        print(f"{player_to_add.fullname} is already in the tournament.")
                    else:
                        confirmation = self.view_main_menu_tracker.confirm_add_player_to_tournament(
                            player_id, player_to_add.fullname
                        )
                        if confirmation == "yes":
                            players_list.append(player_id)
                            self.tournament_to_track.update_tournament_players(
                                players_list,
                                self.tournament_to_track.name,
                                self.tournaments_table,
                                self.database.tournament_query,
                            )
                            print(
                                f"{player_to_add.fullname} has been added to the tournament"
                            )
                except TypeError:
                    print("The player name doesn't exist in the database.")

                # Ask go back to Menu Tracker
                self.view_main_menu_tracker.back_to_tracker_menu()
                clear_console()

            # ----------------------------------------------------------------------
            # User select 'lp-a' to display players in the tournament sort by Alphabet
            # ---------------------------------------------------------------------
            elif user_action_tracker == "lp-a":
                # Sort Players by alphabet
                players_sorted_by_alphabet = self.get_list_players_object()
                players_sorted_by_alphabet.sort(key=lambda player: player.fullname)
                self.view_main_menu_tracker.display_all_players(players_sorted_by_alphabet)

                # Ask go back to Menu Tracker
                self.view_main_menu_tracker.back_to_tracker_menu()
                clear_console()

            # ----------------------------------------------------------------------
            # User select 'lp-r' to display players in the tournament sort by Alphabet
            # ---------------------------------------------------------------------
            elif user_action_tracker == "lp-r":
                # Sort Players by alphabet
                players_sorted_by_rank = self.get_list_players_object()
                players_sorted_by_rank.sort(key=lambda player: player.rank)
                self.view_main_menu_tracker.display_all_players(players_sorted_by_rank)

                # Ask go back to Menu Tracker
                self.view_main_menu_tracker.back_to_tracker_menu()
                clear_console()

            # --------------------------------------
            # User select 'pr' to modify player rank
            # --------------------------------------
            elif user_action_tracker == "pr":
                player_fullname = (
                    self.view_main_menu_tracker.get_player_fullname_to_change_rank()
                )
                player_to_change_rank = Player()
                try:
                    player_to_change_rank.search_by_fullname(
                        player_fullname, self.players_table, self.database.player_query,
                    )

                    is_number = ""
                    new_rank = 0
                    while not is_number:
                        try:
                            new_rank = int(
                                input(
                                    f"Enter new rank for {player_to_change_rank.fullname} : "
                                )
                            )
                            is_number = True
                        except ValueError:
                            print("Please enter a number.")

                    player_to_change_rank.rank = new_rank
                    player_to_change_rank.modify_rank(
                        self.players_table, self.database.player_query
                    )
                    print(
                        f"{player_to_change_rank.fullname} has a new rank: {player_to_change_rank.rank}"
                    )
                except TypeError:
                    print("The player name doesn't exist in the database.")

                # Ask go back to Menu Tracker
                self.view_main_menu_tracker.back_to_tracker_menu()
                clear_console()

            # -------------------------------------------------------
            # User select 'pr' to remove a player from the tournament
            # -------------------------------------------------------
            elif user_action_tracker == "rp":
                player_fullname = (
                    self.view_main_menu_tracker.get_player_fullname_to_remove()
                )

                # Get ID of the player
                player_to_remove = Player()
                try:
                    player_to_remove.search_by_fullname(
                        player_fullname, self.players_table, self.database.player_query
                    )
                    player_id = player_to_remove.get_player_index(
                        player_to_remove.fullname,
                        self.players_table,
                        self.database.player_query,
                    )

                    # Get Tournament players list and check if already in the list
                    players_list = self.tournament_to_track.players

                    if player_id not in players_list:
                        print(f"{player_to_remove.fullname} is not in the tournament.")
                    else:
                        confirmation = self.view_main_menu_tracker.confirm_remove_player_to_tournament(
                            player_id, player_to_remove.fullname
                        )
                        if confirmation == "yes":
                            players_list.remove(player_id)
                            self.tournament_to_track.update_tournament_players(
                                players_list,
                                self.tournament_to_track.name,
                                self.tournaments_table,
                                self.database.tournament_query,
                            )
                            print(
                                f"{player_to_remove.fullname} has been removed to the tournament"
                            )
                except TypeError:
                    print("The player name doesn't exist in the database.")

                # Ask go back to Menu Tracker
                self.view_main_menu_tracker.back_to_tracker_menu()
                clear_console()

            # -------------------------------------------------------------
            # User select 'reset-p' to remove all players to the tournament
            # -------------------------------------------------------------
            elif user_action_tracker == "reset-p":
                # Set players value to empty
                players_list = []
                # Confirm reset
                confirmation = self.view_main_menu_tracker.confirm_reset_players_list()

                if confirmation == "yes":
                    # Update the players database
                    self.tournament_to_track.update_tournament_players(
                        players_list,
                        self.tournament_to_track.name,
                        self.database.tournaments_table,
                        self.database.tournament_query,
                    )









            # -------------------------------------------------------
            # User select 'record' to start recording matches results
            # -------------------------------------------------------
            elif user_action_tracker == "record":
                # Display pairs of matches
                print("-----> ROUND 1 -----> LIST OF MATCHES ----->")
                players_obj_tournament = self.get_list_players_object()
                matches_first_round = self.generate_first_round(players_obj_tournament)
                # Create Round
                round_1 = Round(name="Round 1")
                round_1.define_start_date()
                # Enter Score for every pair of matches
                print("-----> ROUND 1 -----> ENTER SCORE ----->")
                matches_recorded = self.enter_score_first_round(matches_first_round)
                print(type(matches_recorded))
                print(matches_recorded)
                # Ask user confirmation before save matches to round
                confirmation = self.view_main_menu_tracker.confirm_save_round_1_score()
                # If confirmation yes:
                ## save the matches to the round
                ## save the round to the tournament
                if confirmation == "yes":
                    # Save matches to the round
                    round_1.insert_matches(matches_recorded)
                    print(f"Round 1 : {round_1}")
                    self.tournament_to_track.insert_round_to_tournament(round_1)
                    self.tournament_to_track.save_rounds_to_database(
                        round_1,
                        self.tournament_to_track.name,
                        self.tournaments_table,
                        self.database.tournament_query,
                    )














                # Ask to go back to the menu tracker
                self.view_main_menu_tracker.back_to_tracker_menu()
                clear_console()

            else:
                print("sorry your selection doesn't exist")
                back_to_menu = self.view_main_menu_tracker.back_to_tracker_menu()
