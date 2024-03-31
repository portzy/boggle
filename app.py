from boggle import Boggle
from flask import Flask, session, render_template, request, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'akina123'

boggle_game = Boggle()

@app.route('/')
def home():
    """home page"""
    return render_template('welcome.html')

@app.route('/game')
def game():
    """show board"""
    board = boggle_game.make_board()
    session['board'] = board
    return render_template('index.html', board=board)

@app.route('/check-word', methods=['POST'])
def check_word():
    """check if word is in dictionary"""
    guess = request.json['guess'] #extracts word user guessed
    board = session['board'] #retrieves game board from user session
    result = boggle_game.check_valid_word(board, guess)
    print("Result for guess", guess, "is", result)  # temporarily added for debugging
    return jsonify({'result': result})

@app.route('/end-game', methods=['POST'])
def end_game():
    """posts score that was received from front end and updates score and number of plays"""
    current_score = request.json['score']
    session['times_played'] = session.get('times_played', 0) + 1

    highest_score = session.get('highest_score', 0)
    if current_score > highest_score:
        session['highest_score'] = current_score

        return jsonify({
            'times_played': session['times_played'],
            'highest_score': session['highest_score']
        })