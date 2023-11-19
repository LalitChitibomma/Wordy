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
    return render_template('landing.html') 

@app.route("/redirect_join")
def join_game():
    return render_template("join_game.html")

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
    return render_template("game_id.html", msg = game_id)

@app.route("/join_game", methods = ['get'])
def join():
    game_id = request.args.get('game_id')
    if game_id is None:
        return render_template("error.html", msg = "Please enter a valid user id")
    else:
        x = db.get_gameid_content(game_id)
        session['game_id'] = game_id
        terms_and_definitions = [{'term': term, 'definition': definition} for _, term, definition in x]
        return render_template("user_input.html", game_id = game_id, term = terms_and_definitions[0]["term"], increment_id=0)

@app.route('/user_description/<int:increment_id>', methods=['get'])
def result(increment_id):
    if 0 <= increment_id <= 4:
        game_id = session.get('game_id')
        print(game_id)
        game_stuff = db.get_gameid_content(game_id)
        terms_and_definitions = [{'term': term, 'definition': definition} for _, term, definition in game_stuff]
        print(increment_id)
        term_data = terms_and_definitions[increment_id]
        term = term_data['term']
        definition = term_data['definition']
        user_input = request.args.get('user_input')
        data = compare(definition, user_input)
        similarity_score = str(data[0] * 100)[:5] + "%"
        similar_words = data[1] #list of words
        return render_template("user_result.html", actual_term = term, actual = definition, user_input = user_input, similar_words = similar_words, similarity_score=similarity_score, increment_id =increment_id)
    else:
        return render_template("error.html", msg = "Invalid increment_id. Please provide a value between 0 and 5.")
        

@app.route('/increment_index/<int:increment_id>', methods=['GET'])
def increment_index(increment_id):
    print(increment_id)
    next_valid_increment_id = increment_id + 1
    game_id = session.get('game_id')
    game_stuff = db.get_gameid_content(game_id)
    if 0 <= next_valid_increment_id <= 4:
        terms_and_definitions = [{'term': term, 'definition': definition} for _, term, definition in game_stuff]
        term_data = terms_and_definitions[next_valid_increment_id]
        term = term_data['term']
        definition = term_data['definition']
        return render_template('user_input.html', game_id = game_id, term=term,increment_id=next_valid_increment_id)
    else:
        return render_template("done.html", msg = "You are done!")

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()