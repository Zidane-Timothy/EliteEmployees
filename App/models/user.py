from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql.expression import func
from App.database import db

db = SQLAlchemy()

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

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

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
  sequence = db.Column(db.String, nullable = False)
  last_update = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
  

  def get_json(self):
    return {
      'id': self.id,
      'sequence': self.sequence,
      'last_update': self.last_update
    }

  def __init__(self, user_id, word, status, tries):
    self.sequence = sequence
    self.last_update = last_update

