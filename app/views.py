from flask import Blueprint, render_template, request, jsonify, current_app
from werkzeug.utils import secure_filename
from .forms import MovieForm
from .models import Movie
from . import db
import os

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


@views.route('/api/v1/movies', methods=['POST'])
def movies():
    form = MovieForm()

    if form.validate_on_submit():
        poster = form.poster.data
        filename = secure_filename(poster.filename)

        upload_folder = current_app.config['UPLOAD_FOLDER']
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
    return render_template('404.html'), 404