from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
# app.config['SESSION_TYPE'] = 'filesystem'
app.config["SECRET_KEY"] = "HELLO123"
debug = DebugToolbarExtension(app)

boggle_game = Boggle()


@app.route("/")
def make_html_board():
    high_score = session.get("high-score", 0)
    board = boggle_game.make_board()
    session['boggle_board'] = board
    num_played = session.get("num_played", 0)
    return render_template("index.html", board=board, high_score=high_score, num_played=num_played)


@app.route("/check-word", methods=["GET"])
def check_word():
    word = request.args["word"]
    board = session['boggle_board']
    response = boggle_game.check_valid_word(board, word)
    return jsonify({'result': response})


@app.route("/high-score", methods=["POST"])
def high_score():
    high_score = session.get("high-score", 0)

    num_played = session.get("num_played", 0)
    
    score = request.json["score"]
    session["high-score"] = max(high_score, score)
    session["num_played"] = num_played+1
    return jsonify({'high_score': high_score})
