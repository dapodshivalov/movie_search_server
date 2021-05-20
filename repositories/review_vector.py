from repositories.sqlbase import Base, Session, engine
from sqlalchemy import Column, Integer, ARRAY, Float


# Postgres Table
class ReviewVector(Base):
    __tablename__ = 'reviews_vectors'
    __table_args__ = {"schema": "movies"}

    id = Column(Integer, primary_key=True, nullable=False)
    movie_kp_id = Column(Integer, nullable=False)
    review_kp_id = Column(Integer, nullable=False)
    vector = Column(ARRAY(Float), nullable=False)


class ReviewVectorDto:
    def __init__(self, movie_kp_id, review_kp_id, vector):
        self.movie_kp_id = movie_kp_id
        self.review_kp_id = review_kp_id
        self.vector = vector

    def to_dict(self):
        return {
            'movie_kp_id': self.movie_kp_id,
            'review_kp_id': self.review_kp_id,
            'vector': self.vector
        }

    def to_database_entity(self):
        return ReviewVector(
            movie_kp_id=self.movie_kp_id,
            review_kp_id=self.review_kp_id,
            vector=self.vector
        )

    class Deserializer:
        def from_dict(self, dict):
            return ReviewVectorDto(
                dict['movie_kp_id'],
                dict['review_kp_id'],
                dict['vector'],
            )


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    session = Session()
