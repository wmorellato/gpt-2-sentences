from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from ..database import Base

class Genre(Base):
    """Model for genres of stories used to generate
    sentences"""

    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(16), index=True, unique=True)

    def __repr__(self):
        return '<Genre {}>'.format(self.name)

class Sentence(Base):
    """Data model for sentences"""

    __tablename__ = 'sentences'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text)
    genre = Column(Integer, ForeignKey('genres.id'), index=True)
    created = Column(DateTime, default=datetime.now)
    rating = Column(Integer)
    modelVersion = Column(Integer)

    def to_dict(self, **kwargs):
        sentence_dict = {
            'id': self.id,
            'text': self.text,
            'genre': kwargs.get('genre') or self.genre,
            'created': self.created,
            'rating': self.rating,
            'modelVersion': self.modelVersion
        }

        return sentence_dict

    def __repr__(self):
        return '<Sentence, "{}...", genre: {}, created: {}, model: {}, rating: {}>'.format(self.text[:10], self.genre, self.created, self.modelVersion, self.rating)