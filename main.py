from view import View
from models import Player, Tournament, Database



# Create View Object
view = View()
database_system = Database()

# Show Logo Art
view.show_logo()


back_to_menu = "yes"

while back_to_menu == "yes":
    # Get user input
    user_action = view.display_menu().lower()

    # ----- PLAYERS -----
    # CASE 1 : if user input = p : allow user to add a new player to the database
    if user_action == "p":
        # add a new player to the database
        new_player = Player()
        new_player.save_player_to_database()
    # CASE 2 : if user input = pl : allow user to display list of all players in the database
    elif user_action == "pl":
        # display list of all player
        view.display_all_players_database()
    # CASE 3 : if user input = pi : allow user to access detailed info and modification
    elif user_action == "pi":
        view.display_player_information()
    # CASE 4 : if user input = dp : allow user to delete a player from the database
    elif user_action == "dp":
        database_system.remove_player_to_database()
    # ----- TOURNAMENT -----
    # CASE 1 : if user input = t : allow user to create a new tournament to the database
    elif user_action == "t":
        new_tournament = Tournament()
        new_tournament.save_tournament_to_database()
    # CASE 2 : if user input = tl : allow user to display list of all tournaments in the database
    elif user_action == "tl":
        # display list of all tournaments
        view.display_all_tournaments_database()
    # CASE 3 : if user input = ti : allow user to access detailed info and modification
    elif user_action == "ti":
        # display list of all tournaments
        view.display_tournament_information()
    # CASE 4 : if user input = dt : allow user to delete a tournament from the database
    elif user_action == "dt":
        # delete a tournament
        database_system.remove_tournament_to_database()
    else:
        quit()

    back_to_menu = view.back_to_menu()
