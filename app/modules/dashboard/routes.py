from flask import Blueprint, render_template
from app import ESSENTIALS, DATABASE, API_CLIENT
from app.modules.utils import utility
import requests

dash = Blueprint('dash_mod', __name__)


@dash.route('/dashboard', methods=['GET'])
def dashboard():
    food = DATABASE.storage['food']

    if not 'croatian' in food:
        return render_template('dashboard.html', user=ESSENTIALS.session['user'].capitalize(),
                               restaurant=ESSENTIALS.session['restaurant'])
    else:
        if food['menus-no'] < 1:
            food['menus-no'] = 1
            
        return render_template('dashboard-dynamic.html', user=ESSENTIALS.session['user'].capitalize(),
                               restaurant=ESSENTIALS.session['restaurant'], food=food)


@dash.route('/no-internet', methods=['GET'])
def no_internet():
    return render_template('no-internet.html')


@dash.route('/api-error', methods=['GET'])
def api_error():
    return render_template('api-error.html')


@dash.route('/dashboard-sent', methods=['GET'])
def dashboard_sent():
    food = DATABASE.storage['food']
    return render_template('dashboard-dynamic.html', message='Podatci su poslani.',
                           user=ESSENTIALS.session['user'].capitalize(), 
                           restaurant=ESSENTIALS.session['restaurant'],
                           food=food)


@dash.route('/analytics', methods=['GET'])
def dash_analytics():
    # ESSENTIALS.session['restaurant_id']
    if utility.Utility.check_internet():
        try:
            stats = API_CLIENT.get_stats(ESSENTIALS.session['restaurant_id'])
            return render_template('stats.html', user=ESSENTIALS.session['user'].capitalize(),
                                restaurant=ESSENTIALS.session['restaurant'], stats=stats)    
        except requests.exceptions.ConnectionError:
            return render_template('api-error.html')
    return render_template('api-error.html')



