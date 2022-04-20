from datetime import datetime

from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from flaskApp.db import db
from flask_login import UserMixin
from flask_login._compat import unicode



class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False, unique=True)
    authenticated = db.Column(db.Boolean, default=False)
    registered_on = db.Column('registered_on', db.DateTime)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    #roles = db.relationship('Role', secondary='user_roles')
    is_admin = db.Column('is_admin', db.Boolean(), nullable=False, server_default='0')
    songs = db.relationship("Song", back_populates="user", cascade="all, delete")
    locations = db.relationship("Location", back_populates="user", cascade="all, delete")

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.email

    # Define the Role data-model
    # class Role(db.Model):
    #     __tablename__ = 'roles'
    #     id = db.Column(db.Integer(), primary_key=True)
    #     name = db.Column(db.String(50), unique=True)

    # Define the UserRoles association table
    # class UserRoles(db.Model):
    #     __tablename__ = 'user_roles'
    #     id = db.Column(db.Integer(), primary_key=True)
    #     user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    #     role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

class Location():
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=True, unique=False)
    longitude = db.Column(db.String(300), nullable=True, unique=False)
    latitude = db.Column(db.String(300), nullable=True, unique=False)
    population = db.Column(db.Integer, nullable=True, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("User", back_populates="locations", uselist=False)

    def __init__(self, title, longitude, latitude, population):
        self.title = title
        self.longitude = longitude
        self.latitude = latitude
        self.population = population

class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=True, unique=False)
    artist = db.Column(db.String(300), nullable=True, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("User", back_populates="songs", uselist=False)

    def __init__(self, title, artist):
        self.title = title
        self.artist = artist

