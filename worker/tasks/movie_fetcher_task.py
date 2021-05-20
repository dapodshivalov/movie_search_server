import logging

from repositories.film import FilmStatus
from repositories.queue_utils import QueueUtils
from repositories.redis_utils import RedisUtils
from repositories.sqlbase import Session
from worker.date_time_utils import SecondsPeriodBuilder
from worker.fetching.movie_fetcher_utils import get_movie_full_info
from worker.tasks.task import Task


class MovieFetcherTask(Task):
    postgres_session = Session
    redis = RedisUtils

    def __init__(self, queue: QueueUtils, r: RedisUtils):
        self.queue = queue
        self.redis = r
        self.logger = logging.getLogger('taskManager.MovieFetcherTask')

    def name(self):
        return 'MovieFetcherTask'

    def time_period(self):
        return SecondsPeriodBuilder().add_hours(1).build()

    def run(self):
        # TODO redo for movie info

        films = self.queue.get_all_films_from_queue(FilmStatus.RECEIVED)

        # film_by_id = {}

        self.logger.info("Have " + str(len(films)) + " films to fetch")

        movies = []
        for film in films:
            m = get_movie_full_info(film.film_id)
            movies.append(m)
            self.queue.change_film_status(film.film_id, FilmStatus.INFO_FETCHING)

        self.logger.info("Fetched " + str(len(movies)) + " movies")

        for movie in movies:
            self.queue.save_movie_full_info(movie)

            entity_name = 'movie_brief'
            value = movie.get_brief().to_dict()
            identifier = str(movie.kp_id)
            self.redis.save_to_redis(entity_name, identifier, value)

            self.queue.change_film_status(movie.kp_id, FilmStatus.INFO_FETCHED)

        self.logger.info("All movies load")

        # print("{0} reviews received".format(len(reviews)))

        # pbar = tqdm(range(len(reviews)), colour='white')
        # current_film_id = None
        # for i in pbar:
        #     append_review(session, reviews[i])
        #     if current_film_id != reviews[i].movie_id:
        #         if current_film_id is not None:
        #             change_film_status(session, film_by_id[current_film_id], FilmStatus.PROCESSED)
        #         current_film_id = reviews[i].movie_id
        #
        # if current_film_id is not None:
        #     change_film_status(session, film_by_id[current_film_id], FilmStatus.PROCESSED)