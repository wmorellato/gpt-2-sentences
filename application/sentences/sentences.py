from flask import Blueprint, request, jsonify
from flask import current_app as app
from .models import db, Sentence
# from . import scifi_predictor

sentences_bp = Blueprint(
    'sentences_bp', __name__
)

@sentences_bp.route('/scifi/', methods=['GET'])
def scifi_sentences():
    """[summary]
    """
    genre = request.args.get('genre', 'scifi')
    max_length = int(request.args.get('length', 256))

    response = {}

    if genre == 'scifi':
        # result = scifi_predictor.generate(10, length=max_length)
        # response['sentences'] = result

        s = Sentence(
            content='new sentence',
            genre='scifi'
        )

        db.session.add(s)
        db.session.commit()
    
    return jsonify(response)