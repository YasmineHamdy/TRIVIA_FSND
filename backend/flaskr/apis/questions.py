from flask import abort, request, jsonify
import random
from models import Question
from flaskr.apis.categories import get_all_caregories, get_category
from flaskr.apis.helper import paginate

QUESTIONS_PER_PAGE = 10

def setup_questions_apis(app):
    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''
    @app.route('/questions')
    def get_questions():
        questions = Question.query.all()
        current_questions = paginate(request, questions,  QUESTIONS_PER_PAGE)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            'categories': get_all_caregories(),
            'current_category': None,
        })

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):
        questions = Question.query.filter(Question.category == category_id).all()
        current_questions = paginate(request, questions,  QUESTIONS_PER_PAGE)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            'categories': get_all_caregories(),
            'current_category': get_category(category_id),
        })

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''
    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        response = {}

        if(body is None):
            abort(400)

        question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)
        searchTerm = body.get('searchTerm', None)

        
        try:
            if searchTerm:
                questions = Question.query.filter(Question.question.ilike('%{}%'.format(searchTerm))).all()
                current_questions = paginate(request, questions, QUESTIONS_PER_PAGE)
        
                response["questions"] = current_questions
                response["total_questions"] = len(questions)

            else: 
                question = Question(question=question, answer=answer, category=category, difficulty=difficulty)

                question.insert()

                questions = Question.query.all()
                current_questions = paginate(request, questions, QUESTIONS_PER_PAGE)
                
                response["questions"] = current_questions
                response["created"] = question.id
                response["total_questions"] = len(questions)
                
            response["success"] = True

            return jsonify(response)
        except:
            if question and answer and category and difficulty:
                abort(422)
            else:
                abort(400)

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            questions = Question.query.all()
            
            questions = paginate(request, questions, QUESTIONS_PER_PAGE)

            return jsonify({
            'success': True,
            'deleted': question_id,
            'questions': questions,
            'total_questions': len(questions)
            })

        except:
            abort(422)

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():
        body = request.get_json()

        if(body is None):
            abort(400)

        previous_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category', None)


        if not (isinstance(quiz_category, dict) or quiz_category is None):
            abort(400)

        questions = Question.query.filter(Question.category == quiz_category['id']).all() if quiz_category['id'] else Question.query.all()
        is_selected_before = False
        result = {}

        if len(questions) == 0:
            abort(404)
    
        random.shuffle(questions)
        
        for index, random_question in enumerate(questions):
            is_selected_before = random_question.id in previous_questions

            if not is_selected_before:
                result['question'] = random_question.format()
                break
            elif (index == len(questions) - 1 and is_selected_before):
                result['question'] = None
                break
        
        result['success'] = True

        return jsonify(result)
                





