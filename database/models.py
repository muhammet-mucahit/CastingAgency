import os
from sqlalchemy import Column, String, Integer, Enum, Date
from flask_sqlalchemy import SQLAlchemy
import enum

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()


def setup_db(app, database=database_path):
    """
    setup_db(app)
        binds a flask application and a SQLAlchemy service
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = database
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class DatabaseTransactions:
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Movie(db.Model, DatabaseTransactions):
    """
    Movies
    Have title and release date
    """
    __tablename__ = 'Movie'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(Date)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }


class GenderType(enum.Enum):
    """
    GenderType
    Have male and female gender types
    """
    male = 'male'
    female = 'female'


class Actor(db.Model, DatabaseTransactions):
    """
    Actors
    Have name, age and gender
    """
    __tablename__ = 'Actor'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(Enum(GenderType), nullable=False)

    def __init__(self, name, age, gender=GenderType.male):
        self.name = name
        self.age = age
        self.gender = gender

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            # 'gender': self.gender,
        }


class MovieActor(db.Model, DatabaseTransactions):
    """
    MovieActor
    Have movie_id and actor_id
    Many to Many Relationship between Movie and Actor
    """
    __tablename__ = 'MovieActor'

    id = Column(Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("Movie.id"))
    actor_id = db.Column(db.Integer, db.ForeignKey("Actor.id"))

    def __init__(self, movie_id, actor_id):
        self.movie_id = movie_id
        self.actor_id = actor_id

    def format(self):
        return {
            'id': self.id,
            'movie_id': self.movie_id,
            'actor_id': self.actor_id,
        }
