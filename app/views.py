from flask import Blueprint, render_template, request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename
from flask_wtf.csrf import generate_csrf
from .forms import MovieForm
from .models import Movie
from . import db
import os

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


@views.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})


@views.route('/api/v1/movies', methods=['POST'])
def movies():
    form = MovieForm()

    if form.validate_on_submit():
        poster = form.poster.data
        filename = secure_filename(poster.filename)

        upload_folder = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])
        os.makedirs(upload_folder, exist_ok=True)

        poster_path = os.path.join(upload_folder, filename)
        poster.save(poster_path)

        movie = Movie(
            title=form.title.data,
            description=form.description.data,
            poster=filename
        )

        db.session.add(movie)
        db.session.commit()

        return jsonify({
            "message": "Movie Successfully added",
            "title": movie.title,
            "poster": movie.poster,
            "description": movie.description
        }), 201

    return jsonify({
        "errors": form_errors(form)
    }), 400


@views.route('/api/v1/movies', methods=['GET'])
def add_movies():
    movies = Movie.query.all()

    movie_list = []
    for movie in movies:
        movie_list.append({
            "id": movie.id,
            "title": movie.title,
            "description": movie.description,
            "poster": f"/api/v1/posters/{movie.poster}"
        })

    return jsonify({
        "movies": movie_list
    })


@views.route('/api/v1/posters/<filename>', methods=['GET'])
def get_poster(filename):
    upload_folder = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])
    return send_from_directory(upload_folder, filename)


def form_errors(form):
    error_messages = []
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            )
            error_messages.append(message)

    return error_messages


@views.route('/<file_name>.txt')
def send_text_file(file_name):
    file_dot_text = file_name + '.txt'
    return current_app.send_static_file(file_dot_text)


@views.after_app_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@views.app_errorhandler(404)
def page_not_found(error):
    return jsonify({"error": "Page not found"}), 404