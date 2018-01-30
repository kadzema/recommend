

#flask setup
from flask import Flask, jsonify, render_template, request, flash, redirect
app = Flask(__name__)

# connect user_scrape function
from user_scrape import random_forest

@app.route("/")
def home():
    #scrape_dict = collection.find_one()
    return render_template("index.html")

@app.route("/recommend/<username>")
def profile(username):
    user_dict = random_forest(username)
    # return jsonify(user_dict["R2Score"])
    return render_template("recommend.html", 
    profile = user_dict["userProfile"],
    top3 = user_dict["top3UserBeers"],
    recommend = user_dict["recommendations"],
    r2 = round(user_dict["R2Score"] * 100, 2),
    perc = round(user_dict["percCorrect"] * 100, 2))

@app.route("/themagic")
def magic():
    return render_template("the-magic.html")


@app.route("/beerdb")
def allbeers():
    #needs to be adjusted with category selectors
    return render_template("beer-list.html")


@app.route("/about")
def about():
    return render_template("about-us.html")



if __name__ == '__main__':
    app.run(debug=True)