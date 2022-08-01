from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
from datetime import date



config = {
  "apiKey": "AIzaSyA4asYj9YmVNUU2w5mEPlC_eC3sUdEs4F0",
  "authDomain": "test-project-e2c4c.firebaseapp.com",
  "projectId": "test-project-e2c4c",
  "storageBucket": "test-project-e2c4c.appspot.com",
  "messagingSenderId": "494597001768",
  "appId": "1:494597001768:web:936251f57d8ed2a6211b1d",
  "measurementId": "G-Y3SM7CLWVN", 
  "databaseURL": "https://test-project-e2c4c-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


today = date.today()
print("Today's date:", today)

@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email,password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Error with signing up"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = {"email": request.form['email'],"password": request.form['password'],"full_name": request.form['full_name'],"username": request.form['username'], "bio": request.form['bio']}
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email,password)
            db.child("Users").child(login_session['user']['localId']).set(user)
            return redirect(url_for('add_tweet'))
        except:
            error = "Error with signing up"
    return render_template("signup.html", error = error)


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    error = ""
    if request.method == 'POST':
        tweet = {"title": request.form['title'], "text": request.form['text'], "uid": login_session["user"]["localId"]}
        try:
            db.child("Users").child(login_session['user']['localId']).child("Tweets").push(tweet)
            return redirect(url_for('all_tweets'))
        except:
            error = "There was a problem"
    return render_template("add_tweet.html")

@app.route('/all_tweets')
def all_tweets():
    return render_template("all_tweets.html", all_tweets = db.child("Users").child(login_session['user']['localId']).child("Tweets").get().val())

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))



if __name__ == '__main__':
    app.run(debug=True)