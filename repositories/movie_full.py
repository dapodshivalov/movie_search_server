from repositories.movie_brief import MovieBriefDto
from repositories.sqlbase import Base, engine, Session
from sqlalchemy import Column, Integer, String, Text, VARCHAR, ARRAY, Float


# Postgres Table
class MovieFull(Base):
    __tablename__ = 'movies_full_info'
    __table_args__ = {"schema": "movies"}

    id = Column(Integer, primary_key=True, nullable=False)
    kp_id = Column(Integer, nullable=False)
    title = Column(Text, nullable=False)
    rating = Column(Float)
    url = Column(String(256), nullable=False)
    poster_url = Column(String(256))
    year = Column(Integer)
    film_length = Column(String(10))
    slogan = Column(Text)
    description = Column(Text)
    type = Column(String(256))
    rating_mpaa = Column(String(20))
    rating_age_limits = Column(String(20))
    countries = Column(ARRAY(String(256)))
    genres = Column(ARRAY(String(50)))


class MovieFullDto:
    def __init__(self, kp_id, title, rating, url, poster_url, year, film_length, slogan, description, type, rating_mpaa, rating_age_limits, countries, genres):
        self.kp_id = kp_id
        self.title = title
        self.rating = rating
        self.url = url
        self.poster_url = poster_url
        self.year = year
        self.film_length = film_length
        self.slogan = slogan
        self.description = description
        self.type = type
        self.rating_mpaa = rating_mpaa
        self.rating_age_limits = rating_age_limits
        self.countries = countries
        self.genres = genres

    def to_dict(self):
        return {
            'kp_id': self.kp_id,
            'title': self.title,
            'rating': self.rating,
            'url': self.url,
            'poster_url': self.poster_url,
            'year': self.year,
            'film_length': self.film_length,
            'slogan': self.slogan,
            'description': self.description,
            'type': self.type,
            'rating_mpaa': self.rating_mpaa,
            'rating_age_limits': self.rating_age_limits,
            'countries': self.countries,
            'genres': self.genres
        }

    def get_brief(self):
        return MovieBriefDto(self.kp_id, self.title, self.poster_url, self.year, self.rating, self.genres)

    def to_database_entity(self):
        return MovieFull(
            kp_id=self.kp_id,
            title=self.title,
            rating=self.rating,
            url=self.url,
            poster_url=self.poster_url,
            year=self.year,
            film_length=self.film_length,
            slogan=self.slogan,
            description=self.description,
            type=self.type,
            rating_mpaa=self.rating_mpaa,
            rating_age_limits=self.rating_age_limits,
            countries=self.countries,
            genres=self.genres,
        )

    class Deserializer:
        def from_dict(self, dict):
            return MovieFullDto(
                dict['kp_id'],
                dict['title'],
                dict['url'],
                dict['rating'],
                dict['poster_url'],
                dict['year'],
                dict['film_length'],
                dict['slogan'],
                dict['description'],
                dict['type'],
                dict['rating_mpaa'],
                dict['rating_age_limits'],
                dict['countries'],
                dict['genres']
            )


class MovieFullRepository:
    def __init__(self):
        self.session = Session()

    def get_by_kp_id(self, kp_id):
        query = self.session.query(MovieFull).filter(MovieFull.kp_id == kp_id).limit(1)
        return self._entity_to_dto(query[0])

    def get_by_title(self, title):
        query = self.session.query(MovieFull).filter(MovieFull.title == title).limit(1)
        return self._entity_to_dto(query[0])

    @staticmethod
    def _entity_to_dto(entity):
        return MovieFullDto(
            entity.kp_id,
            entity.title,
            entity.rating,
            entity.url,
            entity.poster_url,
            entity.year,
            entity.film_length,
            entity.slogan,
            entity.description,
            entity.type,
            entity.rating_mpaa,
            entity.rating_age_limits,
            entity.countries,
            entity.genres
        )
