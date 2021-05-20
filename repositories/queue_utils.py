from repositories.film import FilmDto, Film, FilmStatus
from repositories.movie_full import MovieFullDto
from repositories.review import ReviewDto, ReviewStatus, Review
from sqlbase import Session


class QueueUtils:
    session = Session

    def __init__(self):
        self.session = Session()

    # APPEND

    def append_film(self, film: FilmDto):
        f = Film(
            film_id=film.film_id,
            title=film.title,
            status=FilmStatus.RECEIVED.value)
        self.session.add(f)
        self.session.commit()

    def append_review(self, review: ReviewDto):
        r = Review(movie_title=review.movie_title,
                   kp_movie_id=review.movie_id,
                   kp_review_id=review.review_id,
                   text=review.text,
                   status=ReviewStatus.RECEIVED.value)
        self.session.add(r)
        self.session.commit()

    def save_movie_full_info(self, movie: MovieFullDto):
        entity = movie.to_database_entity()
        self.session.add(entity)
        self.session.commit()

    # GET

    def get_film_by_kp_id(self, kp_id):
        films = self.session.query(Film).filter(Film.film_id == kp_id).limit(1)
        film_dtos = [FilmDto(film.film_id, film.title) for film in films]
        if len(film_dtos) == 0:
            return None

        film = film_dtos[0]
        return FilmDto(
            film.film_id,
            film.title
        )

    def get_all_films_from_queue(self, status: FilmStatus) -> [FilmDto]:
        films = self.session.query(Film).filter(Film.status == status.value).order_by(Film.id)
        film_dtos = [FilmDto(film.film_id, film.title) for film in films]
        return film_dtos

    def get_all_reviews_from_queue(self, status: ReviewStatus) -> [ReviewDto]:
        reviews = self.session.query(Review).filter(Review.status == status.value).order_by(Review.id)
        review_dtos = [ReviewDto(review.kp_movie_id, review.movie_title, review.kp_review_id, review.text)
                       for review in reviews]
        return review_dtos

    def get_reviews_from_queue(self, status: ReviewStatus, amount) -> [ReviewDto]:
        reviews = self.session.query(Review).filter(Review.status == status.value).order_by(Review.id).limit(amount)
        review_dtos = [ReviewDto(review.kp_movie_id, review.movie_title, review.kp_review_id, review.text)
                       for review in reviews]
        return review_dtos

    def get_films_from_queue(self, status: FilmStatus, amount) -> [FilmDto]:
        films = self.session.query(Film).filter(Film.status == status.value).order_by(Film.id).limit(amount)
        film_dtos = [FilmDto(film.film_id, film.title) for film in films]
        return film_dtos

    # def script_get_reviews(session: Session):
    #     films = get_films_from_queue(session, FilmStatus.RECEIVED, 100)
    #
    #     film_by_id = {}
    #
    #     reviews = []
    #     for film in films:
    #         film_by_id[film.film_id] = film
    #         reviews.extend(get_all_reviews(film, until_page=2))
    #         print(film.title)
    #         change_film_status(session, film, FilmStatus.PROCESSING)
    #
    #     print("{0} reviews received".format(len(reviews)))
    #
    #     pbar = tqdm(range(len(reviews)), colour='white')
    #     current_film_id = None
    #     for i in pbar:
    #         append_review(session, reviews[i])
    #         if current_film_id != reviews[i].movie_id:
    #             if current_film_id is not None:
    #                 change_film_status(session, film_by_id[current_film_id], FilmStatus.PROCESSED)
    #             current_film_id = reviews[i].movie_id
    #
    #     if current_film_id is not None:
    #         change_film_status(session, film_by_id[current_film_id], FilmStatus.PROCESSED)

    # CHANGE

    def change_film_status(self, film_id, status: FilmStatus):
        f = self.session.query(Film).filter(Film.film_id == film_id).first()
        f.status = status.value
        self.session.commit()

    def change_review_status(self, kp_review_id, status: ReviewStatus):
        r = self.session.query(Review).filter(Review.kp_review_id == kp_review_id).first()
        r.status = status.value
        self.session.commit()

    # DELETE

    def delete_movie_by_kp_id(self, kp_id):
        f = self.session.query(Film).filter(Film.film_id == kp_id).first()
        self.session.delete(f)