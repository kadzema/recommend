import pandas as pd
from sqlalchemy import create_engine

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



@app.route('/filter/<filter_col>/<filter_cond>')
def all_beers(filter_col, filter_cond):
    engine = create_engine('postgresql://hgzhyrxbjgjnwa:3fe5e38aa493b4337c39b464fee4a6e71b1e4d33b57a60d50cbe0deaf6ff3e50@ec2-50-16-202-213.compute-1.amazonaws.com:5432/dacosp3h3fd1ng')
    if filter_col == 'all' and filter_cond == 'all':
        df = pd.read_sql("SELECT * FROM beer.beer_feature_all",con=engine)
    else:
        select_statement = f'SELECT * FROM beer.beer_feature_all WHERE "{filter_col}" = ' + f"'{filter_cond}'"
        df = pd.read_sql(select_statement,con=engine)
    df.rename(columns = {"Availaility": "Availability", "num_ratings": "# Ratings", "ReviewCount": "# Reviews", "Ranking": "BA Ranking"}, inplace = True)
    sel_columns = ["Name", "Brewer", "Location", "Style", 'ABV', 'Availability', "Score", "ScoreClass", "pDev", "BA Ranking", "# Ratings", "# Reviews", "URL"]
    df = df[sel_columns]
    df_dict = df.to_dict(orient = 'records')
    return jsonify(df_dict)

if __name__ == '__main__':
    app.run(debug=True)