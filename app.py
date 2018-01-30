

#flask setup
from flask import Flask, jsonify
app = Flask(__name__)

# connect user_scrape function
from user_scrape import random_forest

@app.route("/")
def home():
    #scrape_dict = collection.find_one()
    return "beer stuff"

@app.route("/<username>")
def profile(username):
    user_dict = random_forest(username)
    return jsonify(user_dict)

if __name__ == '__main__':
    app.run(debug=True)