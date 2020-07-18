import os
import csv
from flask import Flask, render_template, jsonify, request
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import dummy
from config import password


# Setup Postgres connection
engine = create_engine(f'postgresql://postgres:{password}@final-project.cft8wszdkeh0.us-east-2.rds.amazonaws.com/postgres')

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
plot_model = Base.classes.omdb

app = Flask(__name__)

""" @app.route("/")
def welcome():
    return  '' """

@app.route("/api/v1.0/genre-form", methods = ['POST'])
def get_genre():
    plot = request.form.get('plot')
    if plot == None:
        return 'Please enter a movie plot'
    # if the plot is not none, send the plot to the machine learning part application
    # get the result and send it to the user
    return dummy.ml_dummy(plot)


@app.route("/api/v1.0/genre-json", methods = ['POST'])
def get_genre_json():
    plot_json = request.get_json()

    # if the plot is not none, send the plot to the machine learning part application
    plot = None
    if 'plot' in plot_json:
        plot = plot_json['plot']
    else:
        return 'Please enter a movie plot'
    # get the result and send it to the user
    return dummy.ml_dummy(plot)


@app.route("/api/v1.0/count-plot")
def genre_count():

    count = {
        "drama": 0,
        "comedy": 0,
        "action": 0,
        "thriller": 0,
        "adventure": 0,
        "horror": 0,
        "fantasy": 0,
        "crime": 0,
        "romance": 0,
        "animation": 0
    }

    with open('model_input.csv', 'r') as csv_file:
        model = csv.reader(csv_file, delimiter=',')
        next(model)

        for row in model:
            if row[1] == "1":
                count["drama"] += 1
            if row[2] == "1":
                count["comedy"] += 1
            if row[3] == "1":
                count["action"] += 1
            if row[4] == "1":
                count["thriller"] += 1
            if row[5] == "1":
                count["adventure"] += 1
            if row[6] == "1":
                count["horror"] += 1
            if row[7] == "1":
                count["fantasy"] += 1
            if row[8] == "1":
                count["crime"] += 1
            if row[9] == "1":
                count["romance"] += 1
            if row[1] == "1":
                count["animation"] += 1       

    return count


@app.route("/api/v1.0/word-count")
def word_count():

    word_counter = []
    with open('model_input.csv', 'r') as csv_file:
        model = csv.reader(csv_file, delimiter=',')
        next(model)

        # word_counter = [len(row[0].split() for row in model]
        for row in model:
            words = row[0].split()
            word_counter.append(len(words))
    
    return jsonify(word_counter)

if __name__ == "__main__":
    app.run(debug=True)