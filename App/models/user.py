from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from App.database import db
from datetime import datetime, time, timedelta
import random
from datetime import datetime
from sqlalchemy.sql.expression import func
from App.database import db



# db = SQLAlchemy()

class GameHistory(db.Model):
    __tablename__ = 'game_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    time_taken = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, game_id, score, time_taken):
        self.user_id = user_id
        self.game_id = game_id
        self.score = score
        self.time_taken = time_taken

    def __repr__(self):
        return '<GameHistory %r>' % self.id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    streak = db.Column(db.Integer, default=0, nullable=False)
    games_won = db.Column(db.Integer, default=0, nullable=False)
    games_played = db.Column(db.Integer, default=0, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
        self.streak = 0
        self.high_score = 0
        self.games_played = 0

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'streak': self.streak,
            'games_won': self.high_score,
            'games_played': self.games_played
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def add_streak(self):
        self.streak += 1

    def add_games_won(self):
        self.games_won += 1

    def add_game_played(self):
        self.games_played += 1

    def new_game(self, game_id):
        game = UserGame.q.filter_by(user_id=self.id, game_id=game_id).first()
      


class UserGame(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable = False)
  tries = db.Column(db.Integer, nullable = False)
  status = db.Column(db.String, nullable = False)

  def get_json(self):
    return {
      'id': self.id,
      'user_id': self.user_id,
      'tries': self.tries,
      'status': self.status
    }

  def __init__(self, user_id, tries, status):
    self.user_id = user_id
    self.tries = tries
    self.status = status

#   def get_tries():
#     self.user_id = user_id
#     self.tries = tries
#     self.status = status

class Game(db.Model):

  id = db.Column(db.Integer, primary_key=True)
  sequence = db.Column(db.String(4), nullable=False)
  last_update = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())  # Changed to store only date

  def get_json(self):
      return {
          'id': self.id,
          'sequence': self.sequence,
          'last_update': self.last_update
      }

  def __init__(self, sequence, last_update):
      self.sequence = sequence
      self.last_update = last_update

  @staticmethod
  def generate_sequence():
      now = datetime.now()
      if now.time() < time(12, 0):
          # If the current time is before 12 AM, use yesterday's date
          today = now.date() - timedelta(days=1)
      else:
          # Otherwise, use today's date
          today = now.date()
      random.seed(today)  # Seed with current date
      sequence = set()  # Use a set to ensure unique digits
      while len(sequence) < 4:
          sequence.add(random.randint(0, 9))
      sequence_str = ''.join(str(digit) for digit in sequence)
      return sequence_str.zfill(4)  # Ensure the sequence has 4 digits

