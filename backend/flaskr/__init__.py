import os
import random

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from models import Category, Question, setup_db

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    ''''This function handles the pagination of questions.'''
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    return questions[start:end]




def create_app():
    
    # create and configure the app
    app = Flask(__name__)
    setup_db(app, os.getenv('DATABASE_URL'))

    # Cors setup for all origins
    CORS(app, resources={r"*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        ''' Use after_request decorator to set Access-Control-Allow '''
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")

        return response
    
    
    @app.route("/categories")
    def get_categories():
        '''This function handles GET requests for all available categories.'''
        try:
            categories = Category.query.all()
            formated_categories = {}
            for category in categories:
                formated_categories[category.id] = category.type

            
            return jsonify({
                "success": True,
                "categories": formated_categories,
                "total_categories": len(categories)
            })
        except Exception:
            abort(404)
            
    @app.route("/categories/<int:category_id>/questions")
    def get_categories_questions(category_id):
        '''This function handles GET requests for questions based on category and paginate.'''
        try:
            questions = Question.query.filter(Question.category == category_id).all()
            current_questions = paginate_questions(request, questions)
            return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": len(questions),
                "current_category": category_id
            })
        except Exception:
            abort(404)
        
            
    
    @app.route("/questions")
    def get_questions():
        '''This endpoint handles GET requests for questions, including pagination (every 10 questions). 
        and returns a list of questions, number of total questions, current category, categories.'''
        try:
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            categories = Category.query.all()

            formated_categories = {}
            for category in categories:
                formated_categories[category.id] = category.type

            return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": len(selection),
                "categories": formated_categories,
                "current_category": None
            })
           
        except Exception:
            abort(404)

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        ''' This endpoint deletes a question using a question ID. '''
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            else:
                question.delete()
                return jsonify ({
                    "success": True,
                    "deleted": question_id
                })

        except Exception:
            abort(422)
            
 
    @app.route("/questions", methods=["POST"])
    def add_questions():
        '''This endpoint will create a new question using the submitted question, answer, difficulty, and category.'''
        
        
        body = request.get_json()

        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_category = body.get("category", None)
        new_difficulty = body.get("difficulty", None)

        try:
            question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
            question.insert()

            return jsonify({
                "success": True,
                "created": question.id
            })
        except Exception:
            abort(422)
            
   
    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        '''
            This endpoint take a search term and return a list of questions that match the search term and paginate.
        '''
        try:
            body = request.get_json()
            search_term = body.get("searchTerm", None)
            print(search_term)
            questions = Question.query.filter(Question.question.ilike(f"%{search_term}%")).all()
            print(questions)
            current_questions = paginate_questions(request, questions)

            return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": len(questions)
            })
        except Exception:
            abort(404)
       

    @app.route("/quizzes", methods=["POST"])
    def play_quiz():
        '''This endpoint take a category and previous question parameters and 
        return a random questions within the given category,
        if provided, and that is not one of the previous questions.'''
        try:
            body = request.get_json()
            previous_questions = body.get("previous_questions", None)
            quiz_category = body.get("quiz_category", None)

            if quiz_category["id"] == 0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter(Question.category == quiz_category["id"]).all()

            questions = [question.format() for question in questions]
            questions = [question for question in questions if question["id"] not in previous_questions]
            question = random.choice(questions) if questions else None

            return jsonify({
                "success": True,
                "question": question
            })
        except Exception:
            abort(422)
            
   
    @app.errorhandler(400)
    def bad_request(error):
        # Handle bad request error (400)
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400


    @app.errorhandler(404)
    def not_found(error):
        # Handle resource not found error (404)
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not Found"
        }), 404


    @app.errorhandler(405)
    def not_allowed(error):
        # Handle method not allowed error (405) 
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405


    @app.errorhandler(422)
    def unprocessable_entity(error):
        # Handle unprocessable entity error (422)
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422


    @app.errorhandler(500)
    def internal_server_error(error):
        # Handle internal server error (500)
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500


    return app

