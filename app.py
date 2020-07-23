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
omdb = Base.classes.omdb

app = Flask(__name__)

@app.route("/")
def home():
    return (render_template("index.html"))

@app.route("/about")
def about():
    return (render_template("about.html"))

@app.route("/graphs")
def graphs():
    return (render_template("graphs.html"))

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
    if 'plot' in plot_json and plot_json['plot'] != "":
        plot = plot_json['plot']
    else:
        return {'error': 'Please enter a movie plot'}, 400
    # get the result and send it to the user
    return dummy.ml_dummy(plot)


@app.route("/api/v1.0/genre-count")
def genre_count():

    session = Session(engine)
    results = session.query(omdb.drama,omdb.comedy,omdb.action,omdb.thriller,omdb.adventure,omdb.horror,omdb.fantasy,omdb.crime,omdb.romance,omdb.animation).all()

    session.close()
    
    genres = {
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

    for drama, comedy, action, thriller, adventure, horror, fantasy, crime, romance, animation in results:
        if drama == 1:
            genres["drama"] += 1
        if comedy == 1:
            genres["comedy"] += 1
        if action == 1:
            genres["action"] += 1
        if thriller == 1:
            genres["thriller"] += 1
        if adventure == 1:
            genres["adventure"] += 1
        if horror == 1:
            genres["horror"] += 1
        if fantasy == 1:
            genres["fantasy"] += 1
        if crime == 1:
            genres["crime"] += 1
        if romance == 1:
            genres["romance"] += 1
        if animation == 1:
            genres["animation"] += 1
    
    return genres
     

@app.route("/api/v1.0/movie-info")
def movie_info():

    session = Session(engine)
    results = session.query(omdb.title,omdb.genre,omdb.plot).all()

    session.close()
    
    movie_info = []
    for title, genre, plot in results:
        movies_dict = {}
        movies_dict["title"] = title
        movies_dict["genre"] = genre.split(", ")
        movies_dict["plot_word_count"] = len(plot.split())
        movie_info.append(movies_dict)

    return jsonify(movie_info)

'''{
   title: "Frozen",
   genre: ["Animation", "Comedy"],
   plot_word_count: 50
}'''

if __name__ == "__main__":
    app.run(debug=True)