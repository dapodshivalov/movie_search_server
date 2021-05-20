from nlp_utils import NlpUtils
from repositories.postgres_utils import PostgresUtils
from repositories.queue_utils import QueueUtils
from tasks.review_processor_task import ReviewProcessorTask
from tasks.task_manager import TaskManager

if __name__ == '__main__':
    task_manager = TaskManager()

    # new_movie_task = AddNewMovieToQueueTask(QueueUtils())
    # movie_fetcher = MovieFetcherTask(QueueUtils(), RedisUtils('127.0.0.1'))
    # review_fetcher = ReviewFetcherTask(QueueUtils())
    review_processor = ReviewProcessorTask(QueueUtils(), NlpUtils(), PostgresUtils())

    # task_manager.add_task(new_movie_task)
    # task_manager.add_task(movie_fetcher)
    # task_manager.add_task(review_fetcher)
    task_manager.add_task(review_processor)

    task_manager.start()
