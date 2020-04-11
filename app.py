from flask import Flask, jsonify, request, abort
from database.models import setup_db, Movie, Actor, GenderType
from flask_cors import CORS
from auth.auth import AuthError, requires_auth
import sys


def create_app(test_config=None):
    app = Flask(__name__)
    app.debug = True
    CORS(app)
    setup_db(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route('/')
    def home():
        return jsonify({
            'success': True
        })

    @app.route('/movies')
    @requires_auth('read:movies')
    def get_all_movies():
        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in Movie.query.all()]
        })

    @app.route('/actors')
    @requires_auth('read:actors')
    def get_all_actors():
        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in Actor.query.all()]
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth('create:movies')
    def add_movie():
        body = request.get_json()

        if 'title' not in body or 'release_date' not in body:
            abort(400)

        actors = []
        if 'actors' in body:
            actor_ids = body['actors']
            for id in actor_ids:
                actors.append(Actor.query.get_or_404(id))

        try:
            title, release_date = body['title'], body['release_date']
            movie = Movie(title, release_date)
            movie.actors = actors
            movie.insert()

            return jsonify({
                'success': True,
                'created': movie.format()
            }), 201
        except:
            print(sys.exc_info())
            abort(422)

    @app.route('/actors', methods=['POST'])
    @requires_auth('create:actors')
    def add_actor():
        body = request.get_json()

        if 'name' not in body or 'age' not in body or 'gender' not in body:
            abort(400)

        try:
            name, age, gender = body['name'], body['age'], body['gender']
            # gender = GenderType.male if gender == 'male' else GenderType.female
            actor = Actor(name, age, gender)
            actor.insert()

            return jsonify({
                'success': True,
                'created': actor.format()
            }), 201
        except:
            print(sys.exc_info())
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('update:movies')
    def update_movie_by_id(movie_id):
        movie = Movie.query.get_or_404(movie_id)
        body = request.get_json()

        if body is None:
            abort(400)

        if 'title' in body:
            movie.title = body['title']

        if 'release_date' in body:
            movie.release_date = body['release_date']

        movie.update()

        return jsonify({
            'success': True,
            'updated': movie.format()
        })

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('update:actors')
    def update_actor_by_id(actor_id):
        actor = Actor.query.get_or_404(actor_id)
        body = request.get_json()

        if body is None:
            abort(400)

        if 'name' in body:
            actor.name = body['name']

        if 'age' in body:
            actor.age = body['age']

        if 'gender' in body:
            actor.gender = body['gender']

        actor.update()

        return jsonify({
            'success': True,
            'updated': actor.format()
        })

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie_by_id(movie_id):
        movie = Movie.query.get_or_404(movie_id)
        movie.delete()
        return jsonify({
            'success': True,
            'deleted': movie_id
        })

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor_by_id(actor_id):
        actor = Actor.query.get_or_404(actor_id)
        actor.delete()
        return jsonify({
            'success': True,
            'deleted': actor_id
        })

    @app.errorhandler(AuthError)
    def unauthorized(error):
        return (
            jsonify({
                "success": False,
                "error": error.status_code,
                "message": error.error
            }),
            error.status_code,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify(
            {
                'success': False,
                'error': 400,
                'message': 'Bad request'
            }
        ), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify(
            {
                'success': False,
                'error': 404,
                'message': 'Not found'
            }
        ), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify(
            {
                'success': False,
                'error': 422,
                'message': 'Unprocessable entity'
            }
        ), 422

    @app.errorhandler(500)
    def server_error(error):
        return (
            jsonify({
                "success": False,
                'error': 500,
                "message": "Server error"
            }),
            500,
        )

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
