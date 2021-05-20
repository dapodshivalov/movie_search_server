from repositories.review_vector import ReviewVectorDto, ReviewVector
from repositories.sqlbase import Session


class PostgresUtils:
    session = Session()

    # GET

    def get_all_review_vectors(self) -> [ReviewVectorDto]:
        vectors = self.session.query(ReviewVector)
        return [ReviewVectorDto(rv.movie_kp_id, rv.review_kp_id, rv.vector) for rv in vectors]

    # SAVE

    def save_review_vector(self, vector: ReviewVectorDto):
        rv = vector.to_database_entity()
        self.session.add(rv)
        self.session.commit(rv)

    # DELETE

    def delete_all_review_vectors_by_review_kp_id(self, review_kp_id) -> int:
        vectors = self.session.query(ReviewVector).filter(ReviewVector.review_kp_id == review_kp_id)
        for v in vectors:
            self.session.delete(v)
        return len(vectors)