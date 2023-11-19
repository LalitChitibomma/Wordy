from Compare import compare
from flask import Flask             #facilitate flask webserving
from flask import render_template, request, redirect   #facilitate jinja templating
from flask import session, url_for, make_response        #facilitate form submission
import os
import db
import random

app = Flask(__name__)    #create Flask object
app.secret_key = os.urandom(32)
db.setup()

@app.route('/')
def index():
    if 'username' in session:
        return redirect("/home")
    return render_template('landing.html') 

@app.route('/login', methods = ['GET','POST'])
def login():
    #Check if it already exists in database and render home page if it does
    #otherwise redirect to error page which will have a button linking to the login page
    username = request.form.get('username')
    password = request.form.get('password')
    if db.verify_account(username,password):
        session['username'] = username
        session['password'] = password
        return redirect("/home")
    else:
        resp = make_response(render_template('error.html',msg = "username or password is not correct"))
        return resp

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        userIn = request.form.get('username')
        passIn = request.form.get('password')
        #print(userIn)
        #print(passIn)
        if db.add_account(userIn, passIn) == -1:
            return render_template("error.html", msg = f"account with username {userIn} already exists")
        else:
            return redirect("/")
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/redirect_join")
def join_game():
    return render_template("join_game.html")

@app.route("/join_game", methods = ['post'])
def join():
    game_id = request.form.get('game_id')
    if game_id is None:
        return render_template("error.html", msg = "Please enter a valid user id")
    else:
        x = db.get_gameid_content(game_id)
        session['game_id'] = game_id
        return render_template("user_input.html", game_id = game_id, contents = x)

@app.route("/create")
def create():
    return render_template("create_game.html")

@app.route("/create_game", methods = ['POST'])
def create_game():
    terms_and_definitions = []
    for i in range(1, 6):
        term = request.form.get(f'term{i}')
        definition = request.form.get(f'definition{i}')
        terms_and_definitions.append({'term': term, 'definition': definition})
    game_id = random.randint(100000,999999)
    for item in terms_and_definitions:
        db.add_game_content(game_id, item['term'], item['definition'])
        #print(f"Term: {item['term']}, Definition: {item['definition']}")
    return render_template("error.html", msg = f"The game id is {game_id}")

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect("/login")
    username = session['username']
    password = session['password']
    if db.verify_account(username, password):
        return render_template("home_page.html", username = username)

@app.route('/user_description/<increment_id>', methods=['POST'])
def result(increment_id):
    game_id = session.get('game_id')
    game_stuff = db.get_gameid_content(game_id)
    
    #print(game_id)
    #print(game_stuff)
    
    terms_and_definitions = [{'term': term, 'definition': definition} for _, term, definition in game_stuff]

    user_input = request.form.get('user_input')
    
    
    data = compare("a thing that is composed of two or more separate elements; a mixture.", user_input)
    similarity_score = data[0]
    similar_words = data[1] #list of words
    return render_template("user_result.html", num=data[0])

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()