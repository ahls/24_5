"""Blogly application."""
from flask import Flask, request, render_template,redirect, flash, session, jsonify

#from flask_debugtoolbar import DebugToolBarExtension
from models import db, connect_db, User,Feedback
from form import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///twitterclone'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'hehe123'

#debug= DebugToolBarExtension(app)
connect_db(app)
with app.app_context():
    db.create_all()

@app.route('/')
def homepage():
    return redirect('/register')
@app.route('/register', methods=['POST','GET'])
def register_post():
    if session.get('userID'):
            return redirect(f'/users/{session["userID"]}')
    form = RegisterForm()
    if form.validate_on_submit(): 
        #if everything checks out, create the user and redirect
        newUser = User.register(form.username.data,form.password.data,form.email.data,form.first_name.data,form.last_name.data)
        db.session.add(newUser)
        db.session.commit()
        session['userID'] = newUser.username
        return redirect(f'/users/{newUser.username}')

    return render_template('register.html', form = form)

@app.route('/login', methods=['POST','GET'])
def login_page():
    if session.get('userID'):
            return redirect(f'/users/{session["userID"]}')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.auth(form.username.data,form.password.data)
        if user:
            session['userID'] = user.username
            return redirect(f'/users/{user.username}')


    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    session.pop('userID')
    return redirect('/login')

@app.route('/users/<username>')
def secret_page(username):
    if session.get('userID') != username:
        flash("you aren't taht person!")
        return redirect('/login')
    
    print(f'useranme: {username}')
    user = User.query.get_or_404(username)
    return render_template('userDetail.html',user=user)

@app.route('/users/<username>/feedback/add', methods=['GET','POST'])
def addFeedbackPage(username):
    if session.get('userID') != username:
        flash('you must be logged in to do that')
        return redirect('/login')
    form = FeedbackForm()
    user = User.query.get_or_404(username)
    if form.validate_on_submit():
        newFeedback = Feedback(title = form.title.data, content = form.content.data, username = username, author = user)
        db.session.add(newFeedback)
        db.session.commit()
        return redirect(f'/users/{username}')
    
    return render_template('addFeedback.html', form=form, user=user)

@app.route('/feedback/<int:feedID>/update', methods=['GET','POST'])
def updateFeedbackPage(feedID):
    feedback = User.query.get_or_404(feedID)
    form = FeedbackForm(obj=feedback)
    if session.get('userID') != feedback.username:
        flash('you must be logged in to do that')
        return redirect('/login')
    if form.validate_on_submit():
        newFeedback = Feedback(title = form.title.data, content = form.content.data, username = username, author = user)
        db.session.add(newFeedback)
        db.session.commit()
        return redirect(f'/users/{username}')
    
    return render_template('editFeedback.html', form=form, feedback = feedback)

@app.route('/feedback/<int:feedID>/delete', methods=['POST'])
def deleteFeedbackPage(feedID):
    feedback = Feedback.query.get_or_404(feedID)
    if session.get('userID') != feedback.username:
        flash('you must be logged in to do that')
        return redirect('/login')

    db.session.delete(feedback)
    db.session.commit()
    
    return redirect(f'/users/{session["userID"]}')

@app.route('/users/<username>/delete', methods=['POST'])
def deleteUser(username):
    if not session.get('userID') or session['userID'] != username:
        flash('you must be logged in to do that')
        return redirect('/login')
    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()
    return redirect('/register')