from flask import Blueprint, request, redirect, render_template, url_for, session, flash
import database as db
from decorators.user import login_required, user_in_room

game_bp = Blueprint('game',
                    __name__,
                    static_folder='../static',
                    template_folder='../templates')


@game_bp.route("/tictactoe/")
def tictactoe():
    return render_template("games/tictactoe.html")


@game_bp.route("/tictactoe/<game_id>")
def get_tictactoe(game_id):
    game = db.get_tictactoe(game_id)

    return game


def str_to_grid(s):
    grid = [["", "", ""], ["", "", ""], ["", "", ""]]
    for i in range(3):
        for j in range(3):
            grid[i][j] = s[i * 3 + j]

    return {"state": grid}


@game_bp.route("/tictactoe/<game_id>/update/<api_key>/<state>",
               methods=["GET"])
# @login_required
def update_tictactoe(game_id, api_key, state):
    state = str_to_grid(state)
    new_state = state['state']
    game = db.get_tictactoe(game_id)
    print(new_state)

    if game is None:
        return "Bad request", 400

    # if 'current_user' in session and session["current_user"] is not None:
    #     if game['next_player'] != session["current_user"] or game['ended']:
    #         return "Bad request", 400
    # elif 'api_key' not in request.form or request.form['api_key'] != 'test':
    #     return "Bad request", 400

    # Ali je sprememba stanja legitimna
    # - natanko 1 sprememba
    # - polje, ki se je spremenilo, je moralo biti prej prazno

    # gremo cez vse elemente
    sprememba = False
    for i in range(3):
        for j in range(3):
            nov_znak = new_state[i][j]  # znak v i-ti vrstici in j-tem stolpcu
            star_znak = game["state"][i][j]

            if nov_znak != star_znak:  # zgodila se je sprememba
                if sprememba or star_znak != "#":
                    return "Bad game state", 400  # ce smo ze prej videli spremembo, ali pa se je spremenilo prej-neprazno polje, koncamo
                sprememba = True

    if sprememba is False:
        return "No change in state", 400

    game['state'] = new_state
    # Ali je kdorkoli zmagal?

    winner = None
    stolpci_sum = ["", "", ""]
    for i in range(3):
        vrstica_sum = ""
        for j in range(3):
            vrstica_sum += game["state"][i][j]
            stolpci_sum[j] += game["state"][i][j]

        # vrstice
        if vrstica_sum == "XXX" or vrstica_sum == "OOO":
            winner = vrstica_sum[0]

    # stolpci
    for sum in stolpci_sum:
        if sum == "XXX" or sum == "OOO":
            winner = sum[0]

    # diagonali
    diag_sum = ["", ""]
    for i in range(3):
        diag_sum[0] += game["state"][i][i]
        diag_sum[1] += game["state"][i][2 - i]

    for sum in diag_sum:
        if sum == "XXX" or sum == "OOO":
            winner = sum[0]

    # V bazo shranimo spremembe

    next_player = game['player_x'] if game['next_player'] == game[
        'player_o'] else game['player_o']
    db.update_tictactoe_state(game_id, game['state'], next_player)

    game['next_player'] = next_player

    if winner is not None:
        winner_player = game["player_x"] if winner == "X" else game["player_o"]

    return "OK", 200
