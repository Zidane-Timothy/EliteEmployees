from celery import Celery
from flask import Flask
from .models import User

@celery.task
def generate_sequence_daily():
    users = User.query.all()
    for user in users:
        user.generate_sequence()
