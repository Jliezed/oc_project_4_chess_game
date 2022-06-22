from models.database import DatabaseChessGame
from models.tournament import Tournament
from models.player import Player
from models.round import Round
from models.match import Match
from views.tracker_view import ViewMainMenuTournamentTracker
from models.console import clear_console


class TournamentTrackerController:
    def __init__(self,):
        """Initialize with models and views"""
        self.view_main_menu_tracker = ViewMainMenuTournamentTracker()
        self.database = DatabaseChessGame()
        self.players_table = self.database.players_table
        self.tournaments_table = self.database.tournaments_table
        self.tournament_query = self.database.tournament_query
        self.player_query = self.database.player_query
        self.tournament_to_track = Tournament()
        self.players_object_list = []

    def get_players_object_list(self):
        """Generate a list of Players Object from Players' IDs
        :return: List of players object
        """
        self.players_object_list = []
        for player_id in self.tournament_to_track.players:
            player = Player()
            player.search_by_index(player_id, self.players_table)
            self.players_object_list.append(player)
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

            player_first_set.opponents.append(player_second_set.id_database)
            player_second_set.opponents.append(player_first_set.id_database)
        return matches_first_round

    def get_score_round(self, matches):
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
        # Sort Players by Score and then by Rank
        self.players_object_list.sort(
            key=lambda player: (-player.cumul_score, player.rank)
        )
        for player in self.players_object_list:
            print(
                f"{player.fullname} - score: {player.cumul_score} - rank {player.rank}"
            )

    def generate_next_round_matches(self):
        """

        :return:
        """
        players_in_matches = []
        matches_next_round = []
        remaining_players_object_list = self.players_object_list[:]

        for player in self.players_object_list:
            if player not in players_in_matches:

                # Get next player
                next_player_index = self.players_object_list.index(player) + 1
                next_player = self.players_object_list[next_player_index]

                # Get next next player in case next player is an opponent
                next_next_player_index = self.players_object_list.index(player) + 2

                # Check if next next player not out of range
                if next_player_index in player.opponents or next_player in players_in_matches:
                    try:
                        next_player = self.players_object_list[next_next_player_index]
                    except IndexError:
                        next_player = remaining_players_object_list[1]
                else:
                    next_player = self.players_object_list[next_player_index]

                # Actions for next player
                players_in_matches.append(next_player)
                remaining_players_object_list.remove(next_player)
                player.opponents.append(next_player.id_database)

                # Actions for current player
                remaining_players_object_list.remove(player)
                players_in_matches.append(player)
                next_player.opponents.append(player.id_database)

                # Display matches
                match = Match(player, next_player)
                match.display_match()
                matches_next_round.append(match)

            else:
                pass
        return matches_next_round

    # ----------------------------------------------------------------------
    # User select 'tt' to Access to other options specific to one tournament
    # ----------------------------------------------------------------------
    def start_menu(self):
        # Ask user the name of the tournament to track
        tournament_name = self.view_main_menu_tracker.get_tournament_name(
            self.tournaments_table, self.tournament_query
        )

        # Retrieve tournament information
        self.tournament_to_track.search_by_name(
            tournament_name, self.tournaments_table, self.tournament_query
        )

        # Initialize Players Object list
        self.get_players_object_list()

        # Reset Players Attributes: Scores & Opponents
        for player in self.players_object_list:
            player.reset_score_opponents(self.players_table, self.player_query)

        # Start Tournament Tracker Menu
        back_to_menu = "yes"
        while back_to_menu == "yes":
            # Get user selection in tournament tracker menu
            user_action_tracker = self.view_main_menu_tracker.display_tracker_menu(
                self.tournament_to_track
            )

            # -------------------------------------------------
            # -------------------- PLAYER ---------------------
            # -------------------------------------------------
            # User select 'a' to Add a player to the tournament
            # -------------------------------------------------
            if user_action_tracker == "a":
                # Ask user the name of the player to add to the tournament
                player_fullname = (
                    self.view_main_menu_tracker.get_player_fullname_to_add()
                )

                player_to_add = Player()
                try:
                    # Search Player in the database and get the ID
                    player_to_add.search_by_fullname(
                        player_fullname, self.players_table, self.player_query
                    )
                    player_id = player_to_add.get_player_index(
                        player_to_add.fullname, self.players_table, self.player_query,
                    )

                    # Get Tournament players list and check if already in the list
                    players_list = self.tournament_to_track.players

                    if len(players_list) == 8:
                        print(
                            "Sorry, you can't add more than 8 players to a tournament. "
                            "Please remove a player "
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
                                self.tournament_query,
                            )
                            print(
                                f"{player_to_add.fullname} has been added to the tournament"
                            )
                except TypeError:
                    print("The player name doesn't exist in the database.")

                # Ask go back to Menu Tracker
                self.view_main_menu_tracker.back_to_tracker_menu()
                clear_console()

            # -----------------------------------------------------------------------
            # User select 'lpa' to display players in the tournament sort by Alphabet
            # -----------------------------------------------------------------------
            elif user_action_tracker == "lpa":
                # Sort Players by alphabet
                players_sorted_by_alphabet = self.get_players_object_list()
                players_sorted_by_alphabet.sort(key=lambda player: player.fullname)
                self.view_main_menu_tracker.display_all_players(
                    players_sorted_by_alphabet
                )

                # Ask go back to Menu Tracker
                self.view_main_menu_tracker.back_to_tracker_menu()
                clear_console()

            # --------------------------------------------------------------------
            # User select 'lpr' to display players in the tournament sort by Rank
            # -------------------------------------------------------------------
            elif user_action_tracker == "lpr":
                # Sort Players by alphabet
                players_sorted_by_rank = self.get_players_object_list()
                players_sorted_by_rank.sort(key=lambda player: player.rank)
                self.view_main_menu_tracker.display_all_players(players_sorted_by_rank)

                # Ask go back to Menu Tracker
                self.view_main_menu_tracker.back_to_tracker_menu()
                clear_console()

            # --------------------------------------
            # User select 'pr' to modify player rank
            # --------------------------------------
            elif user_action_tracker == "pr":
                # Check that record has not been started
                self.tournament_to_track.get_rounds_from_database(
                    self.tournament_to_track.name, self.tournaments_table, self.tournament_query)
                if self.tournament_to_track.rounds == []:
                    player_fullname = (
                        self.view_main_menu_tracker.get_player_fullname_to_change_rank()
                    )
                    player_to_change_rank = Player()
                    try:
                        player_to_change_rank.search_by_fullname(
                            player_fullname, self.players_table, self.player_query,
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
                            self.players_table, self.player_query
                        )
                        print(
                            f"{player_to_change_rank.fullname} has a new rank: "
                            f"{player_to_change_rank.rank}"
                        )
                    except TypeError:
                        print("The player name doesn't exist in the database.")
                else:
                    print(
                        "Record has been started. You can't modify ranks of players. "
                        "Please reset players if you still want to modify ranking"
                    )

                # Ask go back to Menu Tracker
                self.view_main_menu_tracker.back_to_tracker_menu()
                clear_console()

            # -------------------------------------------------------
            # User select 'rp' to remove a player from the tournament
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
                        self.player_query,
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
                                self.tournament_query,
                            )
                            print(
                                f"{player_to_remove.fullname} has been removed to the "
                                f"tournament"
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
                # Set players & rounds values to empty
                players_list = []
                players_details = []
                rounds = []
                # Confirm reset
                confirmation = self.view_main_menu_tracker.confirm_reset_players_list()

                if confirmation == "yes":
                    # Update the players database
                    self.tournament_to_track.update_tournament_players(
                        players_list,
                        self.tournament_to_track.name,
                        self.tournaments_table,
                        self.tournament_query,
                    )
                    # Update players details in the database
                    self.tournament_to_track.update_player_details_database(
                        players_details,
                        self.tournament_to_track.name,
                        self.tournaments_table,
                        self.tournament_query,
                    )
                    # Update rounds in the database
                    self.tournament_to_track.update_rounds_database(
                        rounds,
                        self.tournament_to_track.name,
                        self.tournaments_table,
                        self.tournament_query,
                    )

                # RESET TOURNAMENT INFO
                self.tournament_to_track.search_by_name(
                    self.tournament_to_track.name,
                    self.tournaments_table,
                    self.tournament_query,
                )
            # -------------------------------------------------------
            # User select 'record' to start recording matches results
            # -------------------------------------------------------
            elif user_action_tracker == "record":
                # -----------
                # FIRST ROUND
                # -----------
                # Get rounds from database
                rounds_list = self.tournament_to_track.get_rounds_from_database(
                    self.tournament_to_track.name,
                    self.tournaments_table,
                    self.database.tournament_query,
                )
                # Check if round 1 is in the rounds list gets from the database
                is_round_in_tournament = self.tournament_to_track.is_round_in_tournament(
                    "Round 1", rounds_list
                )
                if not is_round_in_tournament:
                    print("-----> ROUND 1 -----> LIST OF MATCHES ----->")
                    matches_first_round = self.generate_first_round_matches(
                        self.players_object_list
                    )
                    # Create Round
                    round_1 = Round(name="Round 1")
                    round_1.define_start_date()

                    # Enter Score for every pair of matches
                    print("-----> ROUND 1 -----> ENTER SCORE ----->")
                    matches_recorded = self.get_score_round(matches_first_round)

                    # Ask user confirmation before save matches to round
                    confirmation = (
                        self.view_main_menu_tracker.confirm_save_round_score()
                    )
                    if confirmation == "yes":
                        round_1.define_end_date()
                        round_1.matches = matches_recorded
                        print(f"Round 1 : {round_1}")

                        # Save round in tournament database
                        round_dict = round_1.round_to_dict()
                        rounds_list = [round_dict]
                        self.tournament_to_track.update_rounds_database(
                            rounds_list,
                            self.tournament_to_track.name,
                            self.tournaments_table,
                            self.database.tournament_query,
                        )

                        # Save players in tournament database
                        players_details = []
                        for player in self.players_object_list:
                            player.update_player_score_opponents(
                                self.players_table, self.database.player_query
                            )

                            player_details = player.player_details_to_dict()
                            players_details.append(player_details)

                        self.tournament_to_track.update_player_details_database(
                            players_details,
                            self.tournament_to_track.name,
                            self.tournaments_table,
                            self.tournament_query,
                        )

                        # Ask user to exit record
                        exit_record = self.view_main_menu_tracker.display_exit_record()
                        if exit_record == "exit":
                            break
                    else:
                        # Ask to go back to the menu tracker
                        self.view_main_menu_tracker.back_to_tracker_menu()
                        clear_console()

                # ------------
                # NEXT ROUND
                # ------------
                # Get players details of the tournament from the Database
                players_details = \
                    self.tournament_to_track.get_players_details_from_database(
                    self.tournament_to_track.name,
                    self.tournaments_table,
                    self.database.tournament_query,
                )

                # Convert player in players_details into player object
                for player in players_details:
                    player_data = Player()
                    player_data.search_by_index(
                        player["id_database"], self.players_table
                    )
                    # Retrieve Rank, Score and Opponents
                    player_data.rank = player["rank"]
                    player_data.cumul_score = player["cumul_score"]
                    player_data.opponents = player["opponents"]
                    # Update the database
                    player_data.update_player_rank_score_opponents(
                        self.players_table, self.player_query
                    )

                # Re-initiate Players List Object
                self.get_players_object_list()

                # Check if Round is in the rounds list gets from the database
                rounds_names = [f"Round {n}" for n in range(2, 5)]
                for round_name in rounds_names:
                    is_round_in_tournament = self.tournament_to_track.is_round_in_tournament(
                        round_name, rounds_list
                    )
                    if not is_round_in_tournament:
                        print(f"-----> {round_name} -----> LIST OF MATCHES ----->")
                        self.sort_players_by_score_rank()
                        matches_next_round = self.generate_next_round_matches()
                        # Create Round
                        new_round = Round(name=round_name)
                        new_round.define_start_date()
                        # Enter Score for every pair of matches
                        print(f"-----> {round_name} -----> ENTER SCORE ----->")
                        matches_recorded = self.get_score_round(matches_next_round)
                        # Ask user confirmation before save matches to round
                        confirmation = (
                            self.view_main_menu_tracker.confirm_save_round_score()
                        )

                        if confirmation == "yes":
                            new_round.define_end_date()
                            new_round.matches = matches_recorded
                            print(f"{round_name} : {new_round}")
                            rounds_list = self.tournament_to_track.get_rounds_from_database(
                                self.tournament_to_track.name,
                                self.tournaments_table,
                                self.database.tournament_query,
                            )
                            rounds_list.append(new_round.round_to_dict())
                            self.tournament_to_track.update_rounds_database(
                                rounds_list,
                                self.tournament_to_track.name,
                                self.tournaments_table,
                                self.database.tournament_query,
                            )

                            # Save players in tournament
                            players_details = []
                            for player in self.players_object_list:
                                player.update_player_score_opponents(
                                    self.players_table, self.database.player_query
                                )

                                player_details = player.player_details_to_dict()
                                players_details.append(player_details)

                            self.tournament_to_track.update_player_details_database(
                                players_details,
                                self.tournament_to_track.name,
                                self.tournaments_table,
                                self.tournament_query,
                            )

                            # REFRESH PLAYERS OBJECTS
                            self.get_players_object_list()

                            # Ask user to exit record
                            exit_record = (
                                self.view_main_menu_tracker.display_exit_record()
                            )
                            if exit_record == "exit":
                                break

                        else:
                            # Ask to go back to the menu tracker
                            self.view_main_menu_tracker.back_to_tracker_menu()
                            clear_console()
                else:
                    print("All Matches have been recorded.")

                # Ask to go back to the menu tracker
                self.view_main_menu_tracker.back_to_tracker_menu()
                clear_console()

            # ---------------------------------------------------
            # User select 'results' to display tournament results
            # ---------------------------------------------------
            elif user_action_tracker == "results":
                # Get rounds of the tournament from the Database
                rounds = self.tournament_to_track.get_rounds_from_database(
                    self.tournament_to_track.name,
                    self.tournaments_table,
                    self.database.tournament_query,
                )

                # Reformat matches in rounds as [[player_n, score_n], [player_n+1, score_n+1], ...]
                matches_in_rounds_formatted = []
                for r in rounds:
                    matches = r["matches"]
                    for individual_match in matches:
                        playera = individual_match[0]
                        matches_in_rounds_formatted.append(playera)
                        playerb = individual_match[1]
                        matches_in_rounds_formatted.append(playerb)

                # Cumulate scores for each player
                cumul_results = []
                for playerid in self.tournament_to_track.players:
                    cumul_scores = 0
                    for result in matches_in_rounds_formatted:
                        if result[0] == playerid:
                            cumul_scores += result[1]
                    cumul_result_player = (playerid, cumul_scores)
                    cumul_results.append(cumul_result_player)
                cumul_results.sort(key=lambda result: -result[1])

                # Display final results for each player
                print("----- TOURNAMENT RANKING -----")
                for result in cumul_results:
                    id_player = result[0]
                    scores_player = result[1]
                    player_result = Player()
                    player_result.search_by_index(id_player, self.players_table)
                    if cumul_results.index(result) == 0 and scores_player > 0:
                        print(
                            f"The Winner of the Tournament is: {player_result.fullname.upper()}"
                        )

                    print(f"{player_result.fullname} - Score: {scores_player}")

                # Ask to go back to the menu tracker
                self.view_main_menu_tracker.back_to_tracker_menu()
                clear_console()

            # --------------------------------------------------------
            # User select 'dr' to display all rounds of the tournament
            # --------------------------------------------------------
            elif user_action_tracker == "dr":
                self.tournament_to_track.display_rounds(
                    self.tournament_to_track.name,
                    self.tournaments_table,
                    self.tournament_query,
                )

                # Ask to go back to the menu tracker
                self.view_main_menu_tracker.back_to_tracker_menu()
                clear_console()

            # ---------------------------------------------------------
            # User select 'dm' to display all matches of the tournament
            # ---------------------------------------------------------
            elif user_action_tracker == "dm":
                self.tournament_to_track.display_matches(
                    self.tournament_to_track.name,
                    self.tournaments_table,
                    self.tournament_query,
                )

                # Ask to go back to the menu tracker
                self.view_main_menu_tracker.back_to_tracker_menu()
                clear_console()

            # -------------------------------------------------------------
            # User select 'q' to quit
            # -------------------------------------------------------------
            elif user_action_tracker == "q":
                exit()

            else:
                print("sorry your selection doesn't exist")
                back_to_menu = self.view_main_menu_tracker.back_to_tracker_menu()
                if back_to_menu != "yes":
                    exit()
