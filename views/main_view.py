from models.arts import logo
from datetime import datetime


class ViewMainMenu:
    """Main view that display the menu options"""

    def __init__(self):
        pass

    def show_logo(self):
        print(logo)

    def display_menu(self):
        """ Display user options for the main menu"""
        print(
            "---------------------- MENU ----------------------\n"
            "-------------------- CREATION --------------------\n"
            "enter 'p' : Add a player to the database\n"
            "enter 't' : Create a new Tournament\n"
            "-------------------- DATABASE --------------------\n"
            "enter 'pla' : Display list of players by alphabet\n"
            "enter 'plr' : Display list of players by rank\n"
            "enter 'pi' : Access player information\n"
            "enter 'tl' : Display list of tournaments\n"
            "enter 'ti' : Access tournament information\n"
            "--------------- TOURNAMENT TRACKER ---------------\n"
            "enter 'tt' : Track a tournament\n"
            "---------------------- RESET ---------------------\n"
            "enter 'reset' : Reset database\n"
            "--------------------------------------------------\n"
            "Press 'q' to QUIT"
        )

    def back_to_menu(self):
        """ Ask user to go back to the menu """
        back_to_menu = input(
            "Would you like to GO BACK to the MENU? Enter 'yes' or 'no': "
        ).lower()
        return back_to_menu

    # -------------------------------------------------------------
    # User select 'reset' to delete all information in the database
    # -------------------------------------------------------------
    def confirm_reset(self):
        """ Ask user confirmation before to reset the database """
        confirm_reset = input(
            "Are you sure you want to reset the database ? Enter 'yes' or 'no': "
        ).lower()
        return confirm_reset


class ViewMainMenuPlayer:
    """
    View specific to player options in the main menu (add a player to the database,
    display list of players,..)
    """

    def __init__(self):
        self.player_info = {}
        self.save_player = ""

    # ------------------------------------------------
    # User select 'p' to Add a player to the database
    # ------------------------------------------------
    def get_player_info(self):
        """Ask user for player information
        :return: dict of player information
        """
        first_name = input("enter player first name: ").title()
        last_name = input("enter player last name: ").title()

        is_gender = ""
        gender = ""
        while not is_gender:
            gender = input("enter player gender (male/female): ").lower()
            if gender == "male" or gender == "female":
                is_gender = True
            else:
                print("Please enter 'male' or 'female': ")
                is_gender = False

        is_date = ""
        birth_date = ""
        while not is_date:
            try:
                birth_date = input("enter player birth date (DD/MM/YYYY): ")
                birth_date = datetime.strptime(birth_date, "%d/%m/%Y")
                is_date = True
            except ValueError as message_error:
                print(f"*{birth_date}* is not a date format.")
                print(message_error)
        birth_date = birth_date.strftime("%d/%m/%Y")

        rank = 0
        is_int = ""
        while not is_int:
            try:
                rank = int(input("enter player rank (number): "))
                is_int = True
            except ValueError as message_error:
                print(f"*{rank}* is not an integer.")
                print(message_error)

        self.player_info = {
            "first_name": first_name,
            "last_name": last_name,
            "fullname": first_name + " " + last_name,
            "birth_date": birth_date,
            "gender": gender,
            "rank": rank,
        }
        return self.player_info

    def should_save_player(self):
        """ Ask confirmation to save player information to the database"""
        self.save_player = input(
            "Would you like to SAVE the player in the database ? Enter 'yes' or 'no': "
        ).lower()
        return self.save_player

    # -------------------------------------------------------------
    # COMMON:
    # 'pla' to Display list of all players by Alphabet
    # 'plr' to Display list of all players by Rank
    # ---------------------------------------------------------
    def display_all_players(self, players_obj):
        """Display list of all players saved in the database
        :param players_obj: refers to players objects list
        :return: print list of all players in the database
        """
        print("------ LIST OF ALL PLAYERS IN THE DATABASE ------")
        print(f"There are {len(players_obj)} players in the database: ")
        for player in players_obj:
            print(f"Fullname: {player.fullname}\t -\t Rank : {player.rank}")

    # ----------------------------------------------
    # User select 'pi' to Display player information
    # ----------------------------------------------
    def display_player_information(self, players_table, player_query):
        """Display player information for a specific player from user entry
        :param players_table: refers to the player tab in the database
        :param player_query: refers to TinyDB Query
        :return: print player information
        """
        player_fullname = input(
            "Enter player fullname to get his/her information: "
        ).title()
        query_result = players_table.search(player_query.fullname == player_fullname)
        if query_result:
            for item in query_result:
                print(
                    f"\nFullname: {item['fullname']}\n"
                    f"Birth Date: {item['birth_date']}\n"
                    f"Gender: {item['gender']}\n"
                    f"Rank: {item['rank']}\n"
                )
        else:
            print("Sorry, the fullname you enter doesn't exist in the database")

    def back_to_menu(self):
        """ Ask user to go back to the menu """
        back_to_menu = input(
            "Would you like to GO BACK to the MENU? Enter 'yes' or 'no': "
        ).lower()
        return back_to_menu


class ViewMainMenuTournament:
    """
    View specific to tournament option in the main menu (add a tournament to the database, display list of tournaments,..)
    """

    def __init__(self):
        self.tournament_infos = {}
        self.save_tournament = ""

    # ---------------------------------------------------
    # User select 't' to Add a tournament to the database
    # ---------------------------------------------------
    def get_tournament_info(self):
        """Ask user for tournament information
        :return: dict of tournament information
        """
        name = input("enter name of the tournament: ").title()
        location = input("enter location of the tournament: ").title()

        is_date = ""
        date = ""
        while not is_date:
            try:
                date = input("enter date of the tournament (DD/MM/YYYY): ")
                date = datetime.strptime(date, "%d/%m/%Y")
                is_date = True
            except ValueError as message_error:
                print(f"*{date}* is not a date format.")
                print(message_error)
        date = date.strftime("%d/%m/%Y")

        time_control = ""
        is_time_control = ""
        while not is_time_control:
            time_control = input(
                "enter time control of the tournament (bullet / blitz / coup rapide): "
            ).lower()
            if (
                time_control == "bullet"
                or time_control == "blitz"
                or time_control == "coup rapide"
            ):
                is_time_control = True
            else:
                print("Please enter 'bullet' or 'blitz' or 'coup rapide': ")
                is_time_control = False

        description = input("enter description of the tournament: ")

        self.tournament_infos = {
            "name": name,
            "location": location,
            "date": date,
            "time_control": time_control,
            "description": description,
        }
        return self.tournament_infos

    def should_save_tournament(self):
        """ Ask confirmation to save tournament information to the database"""
        self.save_tournament = input(
            "Would you like to SAVE the tournament in the database ? Enter 'yes' or 'no': "
        ).lower()
        return self.save_tournament

    # ---------------------------------------------------
    # User select 'tl' to Display list of all tournaments
    # ---------------------------------------------------
    def display_all_tournaments(self, tournaments_table):
        """Display list of all tournaments saved in the database
        :param tournaments_table: refers to tournament tab from the database
        :return: print a list of all tournaments
        """
        print("----- LIST OF ALL TOURNAMENTS IN THE DATABASE -----")
        print(f"There are {len(tournaments_table)} tournaments in the database:")
        for item in tournaments_table:
            print(
                f"Name: {item['name']} - Located in {item['location']} - {item['date']}"
            )

    # --------------------------------------------------
    # User select 'ti' to Display tournament information
    # --------------------------------------------------
    def display_tournament_information(self, tournaments_table, tournament_query):
        """Display tournament information for a specific tournament from user entry
        :param tournaments_table: refers to the tournament tab in the database
        :param tournament_query: refers to TinyDB query
        :return: print tournament information
        """
        tournament_name = input(
            "Enter tournament name to get more information: "
        ).title()
        query_result = tournaments_table.search(
            tournament_query.name == tournament_name
        )
        if query_result:
            for item in query_result:
                print(
                    f"\nName: {item['name']}\n"
                    f"Location: {item['location']}\n"
                    f"Date: {item['date']}\n"
                    f"Rounds: {item['rounds']}\n"
                    f"Players: {item['players']}\n"
                    f"Players Details: {item['players_details']}\n"
                    f"Time Control: {item['time control']}\n"
                    f"Description: {item['description']}\n"
                )
        else:
            print("Sorry, the name you enter doesn't exist in the database")

    def back_to_menu(self):
        """ Ask user to go back to the menu """
        back_to_menu = input(
            "Would you like to GO BACK to the MENU? Enter 'yes' or 'no': "
        ).lower()
        return back_to_menu
