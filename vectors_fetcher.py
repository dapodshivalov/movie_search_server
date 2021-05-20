from repositories.postgres_utils import PostgresUtils
from repositories.review_vector import ReviewVectorDto


class VectorsFetcher:
    postgres_utils = PostgresUtils

    def __init__(self, postgres_utils: PostgresUtils):
        self.postgres_utils = postgres_utils
        self.vectors = []

    def fetch(self):
        self.vectors = self.postgres_utils.get_all_review_vectors()

    def get(self, only_descriptions=False) -> [dict]:
        vectors = self.vectors
        result = []
        for v in vectors:
            if only_descriptions and v.review_kp_id != -1:
                continue
            result.append({
                'movie_id': v.movie_kp_id,
                'vector': v.vector
            })
        return result
