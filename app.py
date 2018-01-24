# scrape for user profile
from bs4 import BeautifulSoup
import pymongo
import requests

#flask setup
from flask import Flask, jsonify
app = Flask(__name__)

# connect user_scrape function
from user_scrape import user_scrape

@app.route("/")
def home():
    #scrape_dict = collection.find_one()
    return "beer stuff"

@app.route("/<username>")
def profile(username):
    profile, top_3 = user_scrape(username)
    user_list = [profile] + top_3
    return jsonify(user_list)

if __name__ == '__main__':
    app.run(debug=True)