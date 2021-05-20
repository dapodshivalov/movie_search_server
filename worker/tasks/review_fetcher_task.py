import logging

from tqdm import tqdm

from repositories.film import FilmStatus
from repositories.queue_utils import QueueUtils
from repositories.sqlbase import Session
from worker.date_time_utils import SecondsPeriodBuilder
from worker.fetching.review_fetcher_utils import get_k_reviews
from worker.tasks.task import Task


class ReviewFetcherTask(Task):
    _name = 'ReviewFetcherTask'
    postgres_session = Session

    def __init__(self, queue: QueueUtils):
        self.queue = queue
        self.logger = logging.getLogger('taskManager.' + self._name)

    def name(self):
        return self._name

    def time_period(self):
        return SecondsPeriodBuilder().add_hours(5).build()

    # def delay(self):
    #     return SecondsPeriodBuilder().add_minutes(5).build()

    def run(self):
        self.logger.info("Getting movies from queue...")
        films = self.queue.get_all_films_from_queue(FilmStatus.INFO_FETCHED)
        self.logger.info("Got {0} movies from queue".format(len(films)))

        self.logger.info("Getting reviews from KP...")
        reviews_by_film_id = {}
        reviews_count = 0
        # hundreds = 0
        for i in tqdm(range(len(films))):
            film = films[i]
            reviews = get_k_reviews(film.film_id, 4)
            reviews_count += len(reviews)
            # if reviews_count // 100 > hundreds:
            #     hundreds = reviews_count // 100
            #     self.logger.info("Already got {0}".format(reviews_count))
            #     self.logger.info("Last film {0}".format(film.film_id))
            reviews_by_film_id[film.film_id] = reviews
            # self.queue.change_film_status(film.film_id, FilmStatus.REVIEWS_FETCHING)
        self.logger.info("Got {0} reviews from queue".format(reviews_count))

        self.logger.info("Saving reviews to queue...")
        reviews_count = 0
        for film_id, reviews in reviews_by_film_id.items():
            for review in reviews:
                self.queue.append_review(review)
                reviews_count += 1
            self.queue.change_film_status(film_id, FilmStatus.PROCESSED)
        self.logger.info("Saved {0} reviews to queue".format(reviews_count))
