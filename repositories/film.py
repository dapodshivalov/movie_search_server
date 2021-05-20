from enum import Enum

from sqlbase import Base, engine, Session
from sqlalchemy import Column, Integer, String, Text, VARCHAR


class FilmStatus(Enum):
    RECEIVED = "RECEIVED"            # just added to queue
    INFO_FETCHING = "INFO_FETCHING"  # fetching info about movie(genres, cast and e.g.)
    INFO_FETCHED = "INFO_FETCHED"    # info has fetched
    REVIEWS_FETCHING = "REVIEW_FETCHING"        # fetching reviews
    PROCESSED = "PROCESSED"          # all data has fetched


class Film(Base):
    __tablename__ = 'movies_queue'
    __table_args__ = {"schema": "movies"}

    id = Column(Integer, primary_key=True, nullable=False)
    film_id = Column(Integer, nullable=False)
    title = Column(String(100))
    status = Column(String(20))


class FilmDto:
    def __init__(self, film_id, title):
        self._film_id = film_id
        self._title = title

    def to_dict(self):
        return {
            'film_id': self._film_id,
            'title': self._title
        }

    @property
    def title(self):
        return self._title

    @property
    def film_id(self):
        return self._film_id


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    session = Session()