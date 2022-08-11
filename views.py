from flask import Blueprint, render_template, request, redirect, url_for
from .service.query import *

query = Blueprint('query', __name__)


@query.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        food_results = get_foods(request.form.get('foodName'))
        print(food_results)
        return redirect(url_for('query.search', foods=food_results))

    return render_template('index.html')


@query.route('/search', methods=['GET', 'POST'], endpoint='search')
def search():
    return render_template('foodNames.html')
