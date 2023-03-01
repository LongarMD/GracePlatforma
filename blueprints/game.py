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