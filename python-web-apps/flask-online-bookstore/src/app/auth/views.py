from flask import render_template, request, Blueprint, flash, url_for, redirect
from flask_login import login_user, current_user, logout_user, login_required
from threading import Thread
from app import app

from app.models import User
from app.auth.forms import RegisterForm, LoginForm
from app import db

auth = Blueprint('auth', __name__, template_folder='templates')

# register
@auth.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():

        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Thanks for registration!', 'success')

        return redirect(url_for('auth.login'))


    return render_template('auth/register.html', form=form)

    
# login
@auth.route("/login", methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user == None:
            flash("E-mail or password is incorrect!", "danger")
            return render_template("auth/login.html", form=form)

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Successfully logged in!', 'success')

            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('store.home')

            return redirect(next)
    
    return render_template('auth/login.html', form=form)

# logout
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("store.home"))

# Account settings
@auth.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    return render_template('auth/account.html', username=current_user.username, role = current_user.role)



@auth.route("/makeadmin", methods=['GET', 'POST'])
@login_required
def makeadmin():

    if current_user.role == None:
        
        current_user.role = 'admin'
        db.session.commit()

        flash("User was promoted to Admin!", "success")

    else:
        flash("This user is already an Admin!", 'warning')
    
    return redirect(url_for("auth.account"))
