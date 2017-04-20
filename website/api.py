from flask import Flask, Blueprint, flash, redirect, render_template, request, session, url_for
import database
import config

api = Blueprint('api', __name__, template_folder='templates')

@api.route('/api/register', methods=['POST'])
def register():
    try:
        email = request.form['email']
        password = request.form['password']
    except:
        return response('', 400)

    if not database.fetchUser(email) is None:
        error = 'Error: Username already exists'
    else:
        database.addUser(email, password)
        session['user'] = email

        flash('Success: Logging in')
        return redirect(url_for('mysite.index')) 

    return render_template('login.html', error=error)

@api.route('/api/login', methods=['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
    except:
        return response('', 400)

    if not database.validateUser(email, password):
        error = 'Error: Incorrect username or password'
    else:
        session['user'] = email
        flash('Success: Logging in')
        return redirect(url_for('mysite.index'))

    return render_template('login.html', error=error)

@api.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return render_template('login.html', error=None)

@api.route('/api/setVolume', methods=['POST'])
def setVolume():
    config.volume = request.form['volume']
    return ''

@api.route('/api/setTime', methods=['POST'])
def setTime():
    config.time = request.form['time']
    return ''
