# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Documention

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.


### API Endpoints
| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |
| `GET` | `api/questions` | To retrieve all questions, including pagination(every 10 questions) |
| `GET` | `/api/categories` | To retrieve all categories |
| `POST` | `/api/questions` | To create a new questions with text, category and difficulty score |
| `POST` | `/api/categories/{int}/questions` | To retrieve all questions based on category, including pagination(every 10 questions) |
| `POST` | `/api/questions/search` | To retrieve all questions that matches search string |
| `POST` | `/api/quizzes` | This endpoint should take a category and previous question parameters and return a random question within the given category if provided |
| `DELETE` | `/api/questions/{int}` | To delete a single question |


`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns:

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```


`GET '/api/v1.0/questions'`
- Fetches a dictionary of questions in which the keys are the ids and the value is the corresponding string of the question
- Request Arguments: None
- Returns: 

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
  ],
  "total_questions": 19
}
```

`POST '/api/v1.0/categories/<int:category_id>/questions'`
- Fetches a dictionary of questions based on category in which the keys are the ids and the value is the corresponding string of the question
- Request Arguments: None
- Returns:

```json
{
  "current_category": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
  ],
  "total_questions": 4
}
```

`POST '/api/v1.0/questions'`
- Create a new question with text, category and difficulty score
- Request Arguments:
```json
{
  "question": "What is the capital of France?",
  "answer": "Paris",
  "difficulty": 1,
  "category": 3
}
```
- Returns:

```json
{
  "created": 21,
  "success": true
}
```

`POST '/api/v1.0/questions/search'`
- Fetches a dictionary of questions based on search string in which the keys are the ids and the value is the corresponding string of the question
- Request Arguments:
```json
{
  "searchTerm": "title"
}
```
- Returns:

```json
{
  "current_category": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
  ],
  "total_questions": 1
}
```

`POST '/api/v1.0/quizzes'`
- Fetches a random question based on category and previous questions
- Request Arguments:
```json
{
  "previous_questions": [1, 4, 20, 15],
  "quiz_category": {
    "type": "Science",
    "id": "1"
  }
}
```
- Returns:
  
  ```json
  {
    "question": {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 2,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  }
  ```

`DELETE '/api/v1.0/questions/<int:question_id>'`
- Delete a single question based on question id
- Request Arguments: None
- Returns:

```json
{
  "deleted": 21,
  "success": true
}
```


### Status codes

The API is designed to return different status codes according to context and
action. This way, if a request results in an error, the caller is able to get
insight into what went wrong.


| Request type  | Description |
|---------------|-------------|
| `GET`         | Access one or more resources and return the result as JSON. |
| `POST`        | Return `201 Created` if the resource is successfully created and return the newly created resource as JSON. |
| `GET` / `PUT` | Return `200 OK` if the resource is accessed or modified successfully. The (modified) result is returned as JSON. |
| `DELETE`      | Returns `204 No Content` if the resource was deleted successfully. |


