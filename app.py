import time
from boggle import Boggle
from flask import Flask, request, render_template, jsonify, session, flash, make_response
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRETKEYYY123'
app.config['DEBUG_TB_ENABLED'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

boggle_game = Boggle()


@app.route('/boggle')
def displayBoard():
    """Display gameboard"""
    board = boggle_game.make_board()
    session['board'] = board
    highScore = session.get('highScore',0)
    nplays = session.get("nplays", 0)

    return render_template("Gameboard.html", board=board, nplays=nplays, highScore=highScore)


@app.route('/check-word')
def checkWord():
    """check word is valid"""
    word = request.args['word']
    board = session['board']
    res = boggle_game.check_valid_word(board,word)
    return jsonify({'result': res})


@app.route('/game-end', methods=['POST'])
def handleHighScore():
    """If new high-score achieved set to cookie"""
    score = request.json['score']
    currentHighScore = session.get('highScore',0)
    session['highScore'] = max(score, currentHighScore)
    
    nPlays = session.get('nplays',0)
    session['nplays'] = nPlays + 1

    return jsonify(brokeRecord = score > currentHighScore)


