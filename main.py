from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from forms import MovieEditForm, MovieAddForm
from db import Movie, db
import requests
from dotenv import load_dotenv
import os

load_dotenv()

AUTHO_TOKEN = os.getenv('AUTHO_TOKEN')

url_search_endpoint = "https://api.themoviedb.org/3/search/movie"
movie_api_endpoint = "https://api.themoviedb.org/3/movie"
movie_api_images_endpoint = "https://api.themoviedb.org/3/movie/{movie_id}/images"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {AUTHO_TOKEN}"
}

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY')
Bootstrap5(app)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
# initialize the app with the extension
db.init_app(app)

# Create the Tables
with app.app_context():
    db.create_all()


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = MovieAddForm()
    if form.validate_on_submit():
        title = form.title.data
        params = {
            'query': title,
            'include_adult': 'true',
            'language': 'en-US'

        }

        response = requests.get(url_search_endpoint, params=params, headers=headers)
        data = response.json()
        relative_movies = data['results']
        return render_template('select.html', movies=relative_movies)
    return render_template('add.html', form=form)


@app.route('/select')
def select():
    api_movie_id = request.args.get('api_movie_id')
    if api_movie_id:
        movie_api_url = f"{movie_api_endpoint}/{api_movie_id}?language=en-US"
        response = requests.get(movie_api_url, headers=headers)
        data = response.json()
        title = data['original_title']
        img_url = f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}"
        description = data['overview']
        year = data['release_date'].split('-')[0]
        new_movie = Movie(title=title, img_url=img_url, description=description, year=year)
        db.session.add(new_movie)
        db.session.commit()
        print(new_movie.id)
        return redirect(url_for('edit', index=new_movie.id))
        # return render_template('edit.html', index=new_movie.id)


@app.route("/")
def home():
    movies = db.session.execute(db.select(Movie).order_by(Movie.rating)).scalars()
    all_movies = movies.all()

    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", movies=all_movies)


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    form = MovieEditForm()
    index = request.args.get('index')
    print(index)
    movie = db.get_or_404(Movie, index)
    if form.validate_on_submit():
        new_rating = form.rating.data
        new_review = form.review.data
        movie.rating = new_rating
        movie.review = new_review
        db.session.commit()
        db.session.close()
        return redirect(url_for('home'))
    return render_template('edit.html', form=form, movie=movie)


@app.route('/delete')
def delete_movie():
    index = request.args.get('ind')
    movie = db.get_or_404(Movie, index)
    db.session.delete(movie)
    db.session.commit()
    db.session.close()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
