from arts import logo
from tinydb import TinyDB, Query, where

database = TinyDB("database.json")
players_table = database.table("players")
tournaments_table = database.table("tournaments")


class View:
    def show_logo(self):
        print(logo)

    def display_menu(self):
        print("---------------------- MENU ----------------------\n"
              "-------------------- CREATION --------------------\n"
              "enter 'p' : Add a player to the database\n"
              "enter 't' : Create a new Tournament\n"
              "-------------------- DATABASE --------------------\n"
              "enter 'pl' : Display list of players\n"
              "enter 'pi' : Access player information\n"
              "enter 'tl' : Display list of tournaments\n"
              "enter 'ti' : Access tournament information\n"
              "--------------- TOURNAMENT TRACKER ---------------\n"
              "enter 'TT' : Track a tournament\n"
              "-------------------- DELETION --------------------\n"
              "enter 'dp' : Delete a player from the database\n"
              "enter 'dt' : Delete a tournament from the database\n"
              "--------------------------------------------------\n"
              "Press 'q' to QUIT"
              )
        user_action = input("What is you selection ?: ")
        return user_action

    def back_to_menu(self):
        back_to_menu = input("Would you like to GO BACK to the MENU? Enter 'yes' or 'no': ").lower()
        return back_to_menu

    def display_all_players_database(self):
        print("----- LIST OF ALL PLAYERS IN THE DATABASE -----")
        print(f"There are {len(database.table('players'))} players in the database:")
        for item in database.table("players"):
            print(f"Fullname: {item['fullname']}\t -\t Rank : {item['rank']}")

    def display_player_information(self):
        player_query = Query()
        player_fullname = input("Enter player fullname to get his/her information: ").title()
        query_result = database.table("players").search(player_query.fullname == player_fullname)
        if query_result:
            for item in query_result:
                print(f"\nFullname: {item['fullname']}\n"
                      f"Birth Date: {item['birth_date']}\n"
                      f"Gender: {item['gender']}\n"
                      f"Rank: {item['rank']}\n")
        else:
            print("Sorry, the fullname you enter doesn't exist in the database")

    def display_all_tournaments_database(self):
        print("----- LIST OF ALL TOURNAMENTS IN THE DATABASE -----")
        print(f"There are {len(database.table('tournaments'))} tournaments in the database:")
        for item in database.table("tournaments"):
            print(f"Name: {item['name']} - Located in {item['location']} - {item['date']}")

    def display_tournament_information(self):
        tournament_query = Query()
        tournament_name = input("Enter tournament name to get more information: ").title()
        query_result = database.table("tournaments").search(tournament_query.name == tournament_name)
        if query_result:
            for item in query_result:
                print(f"\nName: {item['name']}\n"
                      f"Location: {item['location']}\n"
                      f"Date: {item['date']}\n"
                      f"Rounds: {item['rounds']}\n"
                      f"Players: {item['players']}\n"
                      f"Time Control: {item['time control']}\n"
                      f"Description: {item['description']}\n")
        else:
            print("Sorry, the name you enter doesn't exist in the database")