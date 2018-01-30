import pandas as pd
from sqlalchemy import create_engine

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