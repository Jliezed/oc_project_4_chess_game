from models.round import Round
from models.match import Match
from models.tournament import Tournament
from models.database import DatabaseChessGame
from models.player import Player
from views.tracker_view import ViewMainMenuTournamentTracker
from models.console import clear_console


class TournamentTrackerController:
    def __init__(self, ):
        """Initialize with models from models and views"""
        self.view_main_menu_tracker = ViewMainMenuTournamentTracker()
        self.database = DatabaseChessGame()
        self.players_table = self.database.players_table
        self.tournaments_table = self.database.tournaments_table
        self.rounds_table = self.database.rounds_table
        self.matches_table = self.database.matches_table
        self.tournament_to_track = Tournament()
        self.players_object_list = []

    def get_players_object_list(self):
        """Generate a list of Players Object from Players' IDs
        :return: List of players object
        """
        list_players = self.tournament_to_track.players
        for player_id in list_players:
            player_to_sort = Player()
            player_to_sort.search_by_index(player_id, self.players_table)
            self.players_object_list.append(player_to_sort)
        return self.players_object_list

    def generate_first_round_matches(self, players_object_list):
        """Generate pairs of matches for the first round following Switzerland system.
        :param: players_object_list: list of players object
        :return: list of matches (player a vs player b)
        """
        players_object_list.sort(key=lambda player: player.rank)
        first_set = players_object_list[:4]
        second_set = players_object_list[4:]
        matches_first_round = []
        for player_first_set, player_second_set in zip(first_set, second_set):
            match = Match(player_first_set, player_second_set)
            match.display_match()
            matches_first_round.append(match)

            player_first_set.opponents.append(player_second_set.position)
            player_second_set.opponents.append(player_first_set.position)
        return matches_first_round

    def enter_score_round(self, matches):
        """Ask user scores for each match in the list of matches
        :param matches: list of matches
        :return: list of matches with scores for each player in the match
        """
        matches_recorded = []
        for match in matches:
            match.enter_score()
            match.display_winner()
            match.display_players_score()
            matches_recorded.append(match.players_scores)
        return matches_recorded

    def sort_players_by_score_rank(self):
        """Sort players by score then by rank
        :return: print results
        """
        # Sort Players by Score
        self.players_object_list.sort(key=lambda player: player.score, reverse=True)
        # Then sort by Rank
        self.players_object_list.sort(key=lambda player: player.rank)
        for player in self.players_object_list:
            print(f"{player.fullname} - score: {player.score} - rank {player.rank}")

    def generate_next_round_matches(self):
        copy_players_object_list = self.players_object_list[:]
        players_in_matches = []
        matches_next_round = []

        for player in copy_players_object_list:
            if player not in players_in_matches:
                # Get next player
                next_player_index = copy_players_object_list.index(player) + 1
                next_player = copy_players_object_list[next_player_index]
                # Append to players in match
                players_in_matches.append(player)
                players_in_matches.append(next_player)
                match = Match(player, next_player)
                match.display_match()
                matches_next_round.append(match)

                player.opponents.append(next_player.position)
                next_player.opponents.append(player.position)
            else:
                pass
        return matches_next_round

    def player_opponents(self):
        pass

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

        # Initiate Players Object list
        self.get_players_object_list()

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
                players_sorted_by_alphabet = self.players_object_list
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
                players_sorted_by_rank = self.players_object_list
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
                # -----------
                # FIRST ROUND
                # -----------
                print("-----> ROUND 1 -----> LIST OF MATCHES ----->")
                # Get rounds from database
                rounds_list = self.tournament_to_track.get_rounds_from_database(
                    self.tournament_to_track.name,
                    self.tournaments_table,
                    self.database.tournament_query
                )
                # Check if round 1 is in the rounds list gets from the database
                is_round_in_tournament = self.tournament_to_track.is_round_in_tournament("Round 1", rounds_list)
                if not is_round_in_tournament:
                    matches_first_round = self.generate_first_round_matches(self.players_object_list)
                    # Create Round
                    round_1 = Round(name="Round 1")
                    round_1.define_start_date()
                    # Enter Score for every pair of matches
                    print("-----> ROUND 1 -----> ENTER SCORE ----->")
                    matches_recorded = self.enter_score_round(matches_first_round)
                    # Ask user confirmation before save matches to round
                    confirmation = self.view_main_menu_tracker.confirm_save_round_1_score()
                    if confirmation == "yes":
                        round_1.insert_matches(matches_recorded)
                        print(f"Round 1 : {round_1}")
                        # Save matches in tournament database
                        round_dict = round_1.round_to_dict()
                        rounds_list = [round_dict]
                        self.tournament_to_track.save_rounds_to_database(
                            rounds_list,
                            self.tournament_to_track.name,
                            self.tournaments_table,
                            self.database.tournament_query,
                        )
                        # Save players in tournament database
                        for player in self.players_object_list:
                            player.update_player_score_opponents(self.players_table, self.database.player_query)
                else:
                    pass

                # ------------
                # NEXT ROUND
                # ------------
                # Check if round 2 is in the rounds list gets from the database
                is_round_in_tournament = self.tournament_to_track.is_round_in_tournament("Round 2", rounds_list)
                if not is_round_in_tournament:
                    print("-----> ROUND 2 -----> LIST OF MATCHES ----->")
                    self.sort_players_by_score_rank()
                    matches_second_round = self.generate_next_round_matches()
                    # Create Round
                    round_2 = Round(name="Round 2")
                    round_2.define_start_date()
                    # Enter Score for every pair of matches
                    print("-----> ROUND 2 -----> ENTER SCORE ----->")
                    matches_recorded = self.enter_score_round(matches_second_round)
                    # Ask user confirmation before save matches to round
                    confirmation = self.view_main_menu_tracker.confirm_save_round_1_score()

                    if confirmation == "yes":
                        # Save matches to the round
                        round_2.insert_matches(matches_recorded)
                        print(f"Round 2 : {round_2}")
                        rounds_list = self.tournament_to_track.get_rounds_from_database(
                            self.tournament_to_track.name,
                            self.tournaments_table,
                            self.database.tournament_query
                        )
                        rounds_list.append(round_2.round_to_dict())
                        self.tournament_to_track.save_rounds_to_database(
                            rounds_list,
                            self.tournament_to_track.name,
                            self.tournaments_table,
                            self.database.tournament_query
                        )
                        # Save players in tournament
                        for player in self.players_object_list:
                            player.update_player_score_opponents(self.players_table, self.database.player_query)
                    else:
                        pass

                # Ask to go back to the menu tracker
                self.view_main_menu_tracker.back_to_tracker_menu()
                clear_console()



            # -------------------------------------------------------------
            # -------------------------------------------------------------
            # Enter 'test'
            # -------------------------------------------------------------
            # -------------------------------------------------------------
            elif user_action_tracker == "test":
                pass





                # Ask to go back to the menu tracker
                self.view_main_menu_tracker.back_to_tracker_menu()
                clear_console()


            else:
                print("sorry your selection doesn't exist")
                back_to_menu = self.view_main_menu_tracker.back_to_tracker_menu()
