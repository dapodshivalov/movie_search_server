import logging

from pathlib import Path

from repositories.film import FilmDto
from repositories.queue_utils import QueueUtils
from worker.date_time_utils import SecondsPeriodBuilder
from worker.tasks.task import Task


class AddNewMovieToQueueTask(Task):
    _name = 'AddNewMovieToQueueTask'
    logger = logging.getLogger('taskManager.{0}'.format(_name))
    data_dir = 'tasks/data/new_movies'
    queue = QueueUtils

    def __init__(self, queue: QueueUtils):
        self.queue = queue

    def name(self):
        return self._name

    def time_period(self):
        return SecondsPeriodBuilder().add_minutes(3).build()

    def run(self):
        set_of_ids = set()

        self.logger.info("Getting ids from directory {0}...".format(self.data_dir))
        files = list(Path(self.data_dir).rglob('*.[tT][xX][tT]'))
        for f in files:
            file_name = f.absolute()
            fin = open(file_name, 'r')
            kp_ids = [int(line) for line in fin.readlines()]
            for kp_id in kp_ids:
                set_of_ids.add(kp_id)
        self.logger.info("Got {0} ids from directory".format(len(set_of_ids)))

        kp_ids = sorted(set_of_ids)

        self.logger.info("Saving movies to queue...")
        saved_films_count = 0
        for kp_id in kp_ids:
            film = self.queue.get_film_by_kp_id(kp_id)
            if film is not None:
                continue

            dto = FilmDto(kp_id, None)
            self.queue.append_film(dto)
            saved_films_count += 1
        self.logger.info("Saved {0} movies".format(saved_films_count))