from application import app, db, api
from flask import render_template, json, jsonify, request, Response, redirect, flash, url_for, session
from application.models import User, Course, Enrollment
from application.forms import LoginForm, RegisterForm
from flask_restx import Resource
from application.enrollment_list import enrollment_list


# Global Space
# courseData = [{"courseID":"1111","title":"PHP 101","description":"Intro to PHP","credits":3,"term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":4,"term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":3,"term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":3,"term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":4,"term":"Fall"}]


# API ##################################

# GET ALL
@api.route('/api', '/api/')
class GetAndPost(Resource):
    
    # GET
    def get(self):
        return jsonify(User.objects.all())
    
    # POST
    def post(self):
        data = api.payload

        user = User(user_id=data['user_id'], email=data['email'], first_name=data['first_name'], last_name=data['last_name'])
        user.set_password(data['password'])
        user.save()
        return jsonify(User.objects(user_id = data['user_id']))


# GET ONE (one id)
@api.route('/api/<idx>')
class GetUpdateDelete(Resource):
    
    # GET
    def get(self, idx):
        return jsonify(User.objects(user_id=idx))

    # PUT
    def put(self, idx):
        data = api.payload

        User.objects(user_id = idx).update(**data)
        return jsonify(User.objects(user_id=idx))
    
    # DELETE
    def delete(self, idx):
        User.objects(user_id=idx).delete()
        return jsonify("User successfully deleted!")

########################################


# Route specific space
@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('index.html', index=True)

@app.route('/courses/')
@app.route('/courses/<term>')
def courses(term=None):
    if term is None:
        term = "Spring 2023"

    courseData = Course.objects.order_by("+courseID") # + ascending order, - Descending order.
    return render_template('courses.html', courseData=courseData, courses=True, term=term)

@app.route('/register', methods=['GET', 'POST'])
def register():
    # if session is active
    if session.get('username'):
        return redirect(url_for('index'))
    
    form = RegisterForm()

    if form.validate_on_submit():
        user_id     = User.objects.count()
        user_id     += 1                    # user_id = user_id + 1 

        email       = form.email.data
        password    = form.password.data
        first_name  = form.first_name.data
        last_name   = form.last_name.data

        user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()

        flash("User successfully registered!", "success")
        return redirect(url_for('index'))

    return render_template('register.html', title="Register", form = form, register=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if session is active
    if session.get('username'):
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        email       = form.email.data # request.form.get("email")
        password    = form.password.data

        user = User.objects(email = email).first() # to return a single object
        if user and user.get_password(password):
            flash(f"{user.first_name}, you are sucessfully logged in!", "success")
            session['user_id'] = user.user_id
            session['username'] = user.first_name
            return redirect(url_for('index'))
        else:
            flash("Sorry, something went wrong.", "danger") 
    return render_template('login.html', title="Login", form=form, login=True)



@app.route("/logout")
def logout():
    # Either of them will work 
    session.pop('username', None) # session['user_id'] = False
    return redirect(url_for('index'))


@app.route('/enrollment', methods = ["GET", "POST"])
def enrollment():

    # This page is protected, it will first check if the user is signed in
    if not session.get('username'):
        return redirect(url_for('login'))

    courseID = request.form.get('courseID')
    courseTitle = request.form.get('title')
    user_id = session.get('user_id')

    if courseID:
        if Enrollment.objects(user_id=user_id,courseID=courseID):
            flash(f"You are already registered in this course: {courseTitle}", "danger")
            return redirect(url_for("courses"))
        else:
            Enrollment(user_id=user_id, courseID=courseID).save()
            flash(f"You are enrolled in {courseTitle}!", "success")
    
    classes = enrollment_list(user_id=user_id)


    return render_template('enrollment.html', enrollment=True, title = "Enrollment", classes=classes)


@app.route("/user")
def user():
    #User(user_id=1, first_name="Vlad Andrei", last_name = "Adochitei", email="vladandreiadochitei@gmail.com", password = "abc1234").save()
    #User(user_id=2, first_name="Vladut Andrei", last_name = "Adochitei", email="vlad.adochitei@protonmail.com", password = "abc1234").save()
    users = User.objects.all()
    return render_template("user.html", users = users)