import json
import os
import unittest
from urllib import response

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import Category, Question, setup_db

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.getenv("TEST_DATABASE_URL")
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_categories_404(self):
        """This function tests the get_categories function."""
        response = self.client().get("/categories/1")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not Found")

    def test_get_categories(self):
        """This function tests the get_categories function."""
        response = self.client().get("/categories")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
        self.assertTrue(data["total_categories"])

    def test_get_questions_by_categories(self):
        """This function tests the get_questions_by_categories function."""
        response = self.client().get("/categories/1/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])

    def test_get_questions(self):
        """This function tests the get_questions function."""
        response = self.client().get("/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
        self.assertEqual(data["current_category"], None)

    def test_get_questions_404(self):
        """This function tests the get_questions function."""
        response = self.client().get("/questions/nothing")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not Found")

    def test_add_questions(self):
        """This method tests the add_questions function."""
        response = self.client().post(
            "/questions",
            json={
                "question": "What is the capital of France?",
                "answer": "Paris",
                "difficulty": 1,
                "category": 1,
            },
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])

    def test_search_questions(self):
        """This method tests the search_questions function."""
        response = self.client().post("/questions/search", json={"searchTerm": "1990"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])

    def test_quizzes(self):
        """This method tests the quizzes function."""
        response = self.client().post(
            "/quizzes",
            json={
                "previous_questions": [],
                "quiz_category": {"type": "Science", "id": "1"},
            },
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
