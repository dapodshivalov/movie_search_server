from enum import Enum

from sqlbase import Base, engine, Session
from sqlalchemy import Column, Integer, String, Text, VARCHAR


class ReviewStatus(Enum):
    RECEIVED = "RECEIVED"
    PROCESSED = "PROCESSED"


class Review(Base):
    __tablename__ = 'reviews_queue'
    __table_args__ = {"schema": "movies"}

    id = Column(Integer, primary_key=True, nullable=False)
    movie_title = Column(Text)
    kp_movie_id = Column(Integer, nullable=False)
    kp_review_id = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    status = Column(String(20), nullable=False)

class ReviewDto:
    def __init__(self, movie_id, movie_title, review_id, text):
        self._movie_title = movie_title
        self._movie_id = movie_id
        self._review_id = review_id
        self._text = text

    def to_dict(self):
        return {
            'movie_id': self._movie_id,
            'movie_title': self._movie_title,
            'review_id': self._review_id,
            'text': self._text
        }

    @property
    def review_id(self):
        return self._review_id

    @property
    def movie_title(self):
        return self._movie_title

    @property
    def movie_id(self):
        return self._movie_id

    @property
    def text(self):
        return self._text


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    session = Session()
