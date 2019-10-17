from flask import Blueprint, render_template, redirect, request
from app import ESSENTIALS, DATABASE, API_CLIENT
from app.modules.database import exceptions
from app.modules.utils import utility

import json
import time


login_mod = Blueprint('login_mod', __name__)


@login_mod.route('/', methods=['GET', 'POST'])
@login_mod.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
        
    elif request.method == 'POST':

        user = request.form['username']
        password = request.form['password']
    
        try:
            DATABASE.read()       
            for usr in DATABASE.storage['users']:
                if usr['password'] == password:
                    if usr['username'] == user:
                        ESSENTIALS.session['user'] = user
                        ESSENTIALS.session['restaurant'] = usr['restaurant']

                        ESSENTIALS.session['restaurant_id'] = usr['restaurant_info'].split('/')[-1]
                        
                        food = DATABASE.storage['food']
                        if not 'croatian' in food:
                            return render_template('dashboard.html', user=user.capitalize(), restaurant=usr['restaurant'], food=food)
                        else:
                            if food['menus-no'] < 1:
                                food['menus-no'] = 1
                        return render_template('dashboard-dynamic.html', user=user.capitalize(), restaurant=usr['restaurant'], food=food)                                        
            return render_template('login.html', message="Neispravna lozinka ili korisnisničko ime!")
       
        except (exceptions.DatabaseError):
            return render_template('login.html', message="Prije sljedećeg pokušaja povežite se na internet.")


@login_mod.route('/logout', methods=['GET'])
def logout():
    ESSENTIALS.clear_session()
    return redirect('/login')
