from flask import Flask, render_template, redirect, url_for, request, flash
import tmdb_client
import random
import datetime

movie_types = {

    'popular': 'Popular', 
    'top_rated': 'Top Rated', 
    'now_playing': 'Now Playing', 
    'upcoming': 'Upcoming'
    
}

FAVORITES = set()

app = Flask(__name__)

app.secret_key = b'my-secret-key'

@app.route('/')
def homepage():
    selected_list = request.args.get('list_type', 'popular')
    movies = tmdb_client.get_movies(how_many=8, list_type=selected_list)
    return render_template("homepage.html", movies=movies, current_list=selected_list, movie_types=movie_types)


@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}  

@app.route("/movie/<movie_id>")
def movie_details(movie_id):
    details = tmdb_client.get_single_movie(movie_id)
    cast = tmdb_client.get_single_movie_cast(movie_id)
    movie_images = tmdb_client.get_movie_images(movie_id)
    selected_backdrop = random.choice(movie_images['backdrops'])
    return render_template("movie_details.html", movie=details, cast=cast, selected_backdrop=selected_backdrop)

@app.route('/search')
def search():
    search_query = request.args.get('q', '')
    if search_query:
        movies = tmdb_client.search(search_query=search_query)
    else:
        movies= []
    return render_template('search.html', movies=movies, search_query=search_query)

@app.route('/today')
def today():
     movies = tmdb_client.get_airing_today()
     today = datetime.date.today()
     return render_template('today.html', movies=movies, today=today)

@app.route('/favorites/add', methods=['POST'])
def add_to_favorites():
    data = request.form
    movie_id = data.get('movie_id')
    movie_title = data.get('movie_title')
    if movie_id and movie_title:
        FAVORITES.add(movie_id)
        flash(f'Dodano film {movie_title} do ulubionych.')
    return redirect(url_for('homepage'))

@app.route('/favorites')
def show_favorites():
    if FAVORITES:
        movies = []
        for movie_id in FAVORITES:
            movie_details = tmdb_client.get_single_movie(movie_id)
            movies.append(movie_details)
    else:
        movies = []
        flash(f'Na razie nic tu nie ma.')
    return render_template('favorites.html', movies=movies)

@app.route('/favorites/delete', methods=['POST'])
def delete_from_favorites():
    data = request.form
    movie_id = data.get('movie_id')
    movie_title = data.get('movie_title')
    if movie_id and movie_title:
        FAVORITES.remove(movie_id)
        flash(f'Usunięto {movie_title} z listy ulubionych.')
        return redirect(url_for('show_favorites'))

if __name__ == '__main__':
    app.run(debug=True)

    