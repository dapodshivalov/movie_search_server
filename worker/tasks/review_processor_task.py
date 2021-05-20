import logging

import pandas as pd
from tqdm import tqdm

from nlp_utils import NlpUtils
from repositories.postgres_utils import PostgresUtils
from repositories.queue_utils import QueueUtils
from repositories.review import ReviewStatus
from repositories.review_vector import ReviewVectorDto
from worker.date_time_utils import SecondsPeriodBuilder
from worker.tasks.task import Task


class ReviewProcessorTask(Task):
    _name = 'ReviewProcessorTask'
    queue = QueueUtils
    nlp_utils = NlpUtils
    posgres_utils = PostgresUtils
    logger = logging.getLogger('taskManager.{0}'.format(_name))

    def __init__(self, queue: QueueUtils, nlp_utils: NlpUtils, posgres_utils: PostgresUtils):
        self.queue = queue
        self.nlp_utils = nlp_utils
        self.posgres_utils = posgres_utils

    def name(self):
        return self._name

    def time_period(self):
        return SecondsPeriodBuilder().add_hours(2).build()

    def run(self):
        self.logger.info("Getting reviews from queue...")
        reviews = self.queue.get_all_reviews_from_queue(ReviewStatus.RECEIVED)
        self.logger.info("Got {0} reviews from queue".format(len(reviews)))

        # self.logger.info("Saving to pikle...")
        # columns = ['movie_id', 'movie_title', 'review_id', 'text']
        # n = len(reviews)
        # batch_size = 500
        # for i in range(0, n, batch_size):
        #     size = min(n - i, batch_size)
        #     if i + size < n < i + size + batch_size:
        #         size = n - i
        #         rev_batch = reviews[i:i+size]
        #         data = [r.to_dict() for r in rev_batch]
        #         pd.DataFrame(data, columns=columns).to_pickle('batch_{0}.p'.format(i))
        #         break
        #     rev_batch = reviews[i:i+size]
        #     data = [r.to_dict() for r in rev_batch]
        #     pd.DataFrame(data, columns=columns).to_pickle('batch_{0}.p'.format(i))
        # self.logger.info("Saved")


        self.logger.info("Vectorizing reviews sentences...")
        sentences_count = 0
        sents_by_review_id = {}
        movie_id_by_review_id = {}

        for review in tqdm(reviews):
            movie_id_by_review_id[review.review_id] = review.movie_id

            sents = self.nlp_utils.text_to_vectors(review.text)
            sents_by_review_id[review.review_id] = sents

            sentences_count += len(sents)
        self.logger.info("Vectorized {0} sentences".format(sentences_count))

        self.logger.info("Saving reviews sentences vectors to DB")
        saved_vectors_count = 0
        for review_id, sentences in tqdm(sents_by_review_id.items()):
            movie_id = movie_id_by_review_id[review_id]

            deleted_counts = self.posgres_utils.delete_all_review_vectors_by_review_kp_id(review_id)
            if deleted_counts > 0:
                self.logger.info("Deleted previous {0} vectors".format(deleted_counts))

            for vector in sentences:
                rv_dto = ReviewVectorDto(movie_id, review_id, vector)
                self.posgres_utils.save_review_vector(rv_dto)
                saved_vectors_count += 1
            self.queue.change_review_status(review_id, ReviewStatus.PROCESSED)
        self.logger.info("Saved {0} vectors".format(saved_vectors_count))
