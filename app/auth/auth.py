from flask import render_template, flash, redirect, url_for, Blueprint, request
from flask_login import login_user, logout_user, login_required, current_user

from app.extensions import db
from app.models import User

auth_blue = Blueprint('auth', __name__, url_prefix="/auth", template_folder="templates", static_folder="static")


@auth_blue.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chat.index'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember_me = request.form.get('remember', False)

        if remember_me:
            remember_me = True

        user = User.query.filter_by(email=email).first()

        if user is not None:
            if user.password_hash is None:
                flash('Please use the third party service to log in.')
                return redirect(url_for('.login'))

            if user.verify_password(password):
                login_user(user, remember_me)
                return redirect(url_for('chat.index'))
        flash('Either the email or password was incorrect.')
        return redirect(url_for('.login'))

    return render_template('auth.login.html')


@auth_blue.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('chat.index'))


@auth_blue.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('chat.index'))

    if request.method == 'POST':
        email = request.form['email'].lower()

        user = User.query.filter_by(email=email).first()
        if user is not None:
            flash('The email is already registered, please log in.')
            return redirect(url_for('.login'))

        nickname = request.form['nickname']
        password = request.form['password']

        user = User(nickname=nickname, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('chat.index'))

    return render_template('auth.register.html')