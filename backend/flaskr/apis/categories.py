
from flask import jsonify
from models import Category

def get_all_caregories():
    categories = Category.query.all()
    formatedCategories =  {}

    for category in categories:
        formatedCategories[category.id] = category.type

    return formatedCategories

def get_category(category_id):
    category = Category.query.get(category_id)
    return category.format()

def setup_categories_apis(app):
    '''
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''
    @app.route('/categories')
    def get_categories():

        return jsonify({
            'success': True,
            'categories': get_all_caregories()
        })