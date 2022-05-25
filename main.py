from view import (
    ViewMainMenu,
    ViewMainMenuPlayer,
    ViewMainMenuTournament,
    ViewMainMenuTournamentTracker,
)
from models import Player, DatabaseChessGame, Tournament
from controller import Controller

database_chess_game = DatabaseChessGame()
view_main_menu = ViewMainMenu()
view_main_menu_player = ViewMainMenuPlayer()
view_main_menu_tournament = ViewMainMenuTournament()
view_main_menu_tournament_tracker = ViewMainMenuTournamentTracker()
player = Player()
tournament = Tournament()
controller = Controller(
    view_main_menu,
    view_main_menu_player,
    view_main_menu_tournament,
    view_main_menu_tournament_tracker,
    database_chess_game,
    player,
    tournament,
)

controller.start_program()
