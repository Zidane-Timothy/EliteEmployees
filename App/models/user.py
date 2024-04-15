from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql.expression import func
from App.database import db

#db = SQLAlchemy()

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

class Game(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  sequence = db.Column(db.String(4), nullable = False)
  last_update = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
  

  def get_json(self):
    return {
      'id': self.id,
      'sequence': self.sequence,
      'last_update': self.last_update
    }

  def __init__(self, sequence, last_update):
    self.sequence = sequence
    self.last_update = last_update

  def generate_sequence():
    sequence = ''
    for i in range(4):
      sequence += str(random.randint(0,9))
    return sequence
  
  # def generate_unique_sequence():
  #   digits = list(range(10))  # Create a list of digits from 0 to 9
  #   random.shuffle(digits)    # Shuffle the list randomly
  #   unique_sequence = ''.join(map(str, digits[:4]))  # Take the first 4 digits
  #   return unique_sequence
