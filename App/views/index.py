
from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db, Game

from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, session
from App.models import db


from App.controllers import create_user, update_user, get_all_users, get_all_users_json, get_user_by_username, get_user

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
    # Get past_rows from the session, or initialize it if it doesn't exist
    past_rows = session.get('past_rows', [])

    if request.method == 'POST':
      secret_number = "1234"  # Replace with your actual secret number
      guesses_remaining = 6 #How many guesses are we using?

      # Obtain the user's guess from the form inputs
      guess1 = request.form.get('guess1')
      guess2 = request.form.get('guess2')
      guess3 = request.form.get('guess3')
      guess4 = request.form.get('guess4')

      guess = guess1 + guess2 + guess3 + guess4
      result = check_guess(secret_number, guess)

      guesses_remaining -= 1

      # Append the current guess and its result to the list of past rows
      past_rows.append({"guess": guess, "result": result})

      # Save past_rows back to the session
      session['past_rows'] = past_rows

      # Check if the player has won
      if result == ["green", "green", "green", "green"]:
          return jsonify({"result": "Congratulations! You've won the game!"})

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
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})
