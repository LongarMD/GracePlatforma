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

@game_bp.route("/tictactoe/<game_id>/update", methods=["POST"])
def update_tictactoe(game_id):
    new_state = request.form["state"]
    game = db.get_tictactoe(game_id)

    if game['next_player'] != session["current_user"]:
        return False