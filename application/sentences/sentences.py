import random
from flask import Blueprint, request, jsonify
from flask import current_app as app
from flask_cors import cross_origin
from sqlalchemy import func
from markupsafe import escape
from .models import Sentence, Genre

sentences_bp = Blueprint(
    'sentences_bp', __name__
)

@sentences_bp.route('/sentences/<genre>', methods=['GET'])
def get_sentences(genre):
    """
        Get a list of generated sentences by genre.
    """
    num_samples = int(request.args.get('ns', 5))

    if num_samples > 20:
        num_samples = 20

    indexes = []
    response = []
    count = app.db_session.query(func.count(Sentence.id)).scalar()

    if count > 0:
        indexes = random.choices(range(count), k=num_samples)
    
    sentences = app.db_session.query(Sentence).join(Genre, genre == Genre.name).filter(Sentence.id.in_(indexes)).all()

    for s in sentences:
        response.append(s.to_dict(genre=genre))

    return jsonify(response)