"""Models"""
from .. import db

class Genre(db.Model):
    """Model for genres of stories used to generate
    sentences"""

    __tablename__ = 'genres'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(16),
        primary_key=True,
        index=True,
        unique=True
    )

class Sentence(db.Model):
    """Data model for sentences"""

    __tablename__ = 'sentences'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    content = db.Column(
        db.Text
    )

    genre = db.Column(
        db.Integer,
        db.ForeignKey('genres.id')
    )