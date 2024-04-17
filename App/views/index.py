from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db, Game
from App.controllers import create_user, update_user, get_all_users, get_all_users_json, get_user_by_username, get_user
from datetime import datetime  # Import datetime here

index_views = Blueprint('index_views', __name__, template_folder='../templates')

def check_guess(secret_number, guess):
    result = []
    for i, digit in enumerate(guess):
        if digit in secret_number:
            if digit == secret_number[i]:
                result.append("green")  # Correct digit in correct position
            else:
                result.append("yellow")  # Correct digit in wrong position
        else:
            result.append("black")  # Digit not in secret number
    return result

@index_views.route('/', methods=['GET','POST'])
def index_page():

    past_rows = ["grey","grey","grey","grey"]  # List to store past guesses and their results

    if request.method == 'POST':
        game = Game.query.first()
        if game is None:
            # If there's no game in the database, create a new one
            sequence = Game.generate_sequence()
            game = Game(sequence=sequence, last_update=datetime.now().date())
            db.session.add(game)
            db.session.commit()

        secret_number = game.sequence  # Get the secret number from the database
        print(secret_number)
        guesses_remaining = 6  # How many guesses are we using?

        # Obtain the user's guess from the form inputs
        guess1 = request.form.get('guess1')
        guess2 = request.form.get('guess2')
        guess3 = request.form.get('guess3')
        guess4 = request.form.get('guess4')

        guess = guess1 + guess2 + guess3 + guess4
        result = check_guess(secret_number, guess)

        guesses_remaining -= 1

        # Append the current guess and its result to the list of past rows
        past_rows.append(result)

        # Check if the player has won
        if result == ["green", "green", "green", "green"]:
            return jsonify({"result": "Congratulations! You've won the game!"}) # create a redirect URL

        # Check if the player has lost
        if guesses_remaining == 0:
            return jsonify({"result": "Sorry, you've run out of guesses. The secret number was: " + secret_number})

        # Prepare response with result, remaining guesses, and past rows
        response = {
            "result": result,
            "guesses_remaining": guesses_remaining,
            "past_rows": past_rows
        }
        return render_template('index.html', past_rows=past_rows, guesses_remaining=guesses_remaining)

    return render_template('index.html', past_rows=past_rows)


@index_views.route('/init', methods=['GET']) #works
def init():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    # Generate a new sequence and save it to the database
    sequence = Game.generate_sequence()
    game = Game(sequence=sequence, last_update=datetime.now().date())
    db.session.add(game)
    db.session.commit()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})
