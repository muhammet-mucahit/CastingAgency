import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import setup_db


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['TEST_DATABASE_URL']
        setup_db(self.app, self.database_path)

        self.casting_assistant_jwt = os.environ['CASTING_ASSISTANT']
        self.casting_director_jwt = os.environ['CASTING_DIRECTOR']
        self.executive_producer_jwt = os.environ['EXECUTIVE_PRODUCER']

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    def test_get_all_movies(self):
        res = self.client().get("/movies", headers={
            "Authorization": "Bearer {}".format(self.casting_assistant_jwt)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])

    def test_get_all_actors(self):
        res = self.client().get("/actors", headers={
            "Authorization": "Bearer {}".format(self.casting_assistant_jwt)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])

    def test_add_movie(self):
        res = self.client().post("/movies", json={
            "title": "My Life",
            "release_date": "07.20.2020"
        }, headers={
            "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])

    def test_401_unauthorized_add_movie(self):
        res = self.client().post("/movies", json={
            "title": "My Life",
            "release_date": "07.20.2020"
        }, headers={
            "Authorization": "Bearer {}".format(self.casting_assistant_jwt)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 401)
        self.assertTrue(data["message"])

    def test_422_add_movie_with_wrong_date_format(self):
        res = self.client().post("/movies", json={
            "title": "My Life",
            "release_date": "20.07.2020"
        }, headers={
            "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 422)

    def test_add_actor(self):
        res = self.client().post("/actors", json={
            "name": "My Life",
            "age": 27,
            "gender": "male"
        }, headers={
            "Authorization": "Bearer {}".format(self.casting_director_jwt)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])

    def test_400_add_actor_without_required_name_parameter(self):
        res = self.client().post("/actors", json={
            "age": 27,
            "gender": "male"
        }, headers={
            "Authorization": "Bearer {}".format(self.casting_director_jwt)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 400)

    # def test_get_movie(self):
    #     res = self.client().get("/movies/1")
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["movie"])
    #
    # def test_404_get_movie_which_does_not_exist(self):
    #     res = self.client().patch("/movies/5")
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["error"], 404)
    #
    # def test_get_actor(self):
    #     res = self.client().get("/actors/1")
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["movie"])
    #
    # def test_404_get_actor_which_does_not_exist(self):
    #     res = self.client().patch("/actors/5")
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["error"], 404)

    def test_update_movie(self):
        res = self.client().patch("/movies/4", json={
            "title": "My Life is Over",
        }, headers={
            "Authorization": "Bearer {}".format(self.casting_director_jwt)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["updated"])

    def test_404_update_movie_which_does_not_exist(self):
        res = self.client().patch("/movies/1000", json={
            "title": "My Life is Over",
        }, headers={
            "Authorization": "Bearer {}".format(self.casting_director_jwt)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)

    def test_update_actor(self):
        res = self.client().patch("/actors/3", json={
            "age": 35,
        }, headers={
            "Authorization": "Bearer {}".format(self.casting_director_jwt)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["updated"])

    def test_404_update_actor_which_does_not_exist(self):
        res = self.client().patch("/actors/1000", json={
            "age": 35,
        }, headers={
            "Authorization": "Bearer {}".format(self.casting_director_jwt)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)

    def test_401_unauthorized_delete_movie(self):
        res = self.client().delete("/movies/1", headers={
            "Authorization": "Bearer {}".format(self.casting_director_jwt)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 401)
        self.assertTrue(data["message"])

    def test_delete_movie(self):
        res = self.client().delete("/movies/2", headers={
            "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["deleted"])

    def test_404_delete_movie_which_does_not_exist(self):
        res = self.client().delete("/movies/1", headers={
            "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)

    def test_delete_actor(self):
        res = self.client().delete("/actors/2", headers={
            "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["deleted"])

    def test_404_delete_actor_which_does_not_exist(self):
        res = self.client().delete("/actors/1", headers={
            "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
