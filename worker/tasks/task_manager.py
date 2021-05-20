import datetime
import time
from threading import Thread
import logging
import logging.config
from os import path
import traceback

from worker.tasks.task import Task

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'config/logger.conf')
logging.config.fileConfig(log_file_path)
logger = logging.getLogger("taskManager")


class TaskManager:
    next_id = int
    task_by_id = {}
    last_launch_by_id = {}
    is_launched = {}

    def __init__(self):
        self.next_id = 0

    def add_task(self, task: Task):
        self.task_by_id[self.next_id] = task
        self.last_launch_by_id[self.next_id] = None
        if task.delay() != 0:
            self.last_launch_by_id[self.next_id] = time.time() - (task.time_period() - task.delay())
        self.is_launched[self.next_id] = False
        self.next_id += 1

    def start(self):
        indexes = self.task_by_id.keys()
        while True:
            for task_index in indexes:
                task = self.task_by_id[task_index]
                last_launch_time = self.last_launch_by_id[task_index]

                if self._should_launch(task_index, task, last_launch_time):
                    self.is_launched[task_index] = True
                    self.last_launch_by_id[task_index] = time.time()
                    self._async_launch(task_index, task)

    def _should_launch(self, task_id, task, last_launch) -> bool:
        if self.is_launched[task_id]:
            return False
        now = time.time()
        if last_launch is None:
            return True
        return (now - last_launch) >= task.time_period()

    def _async_launch(self, task_id, task: Task):
        task_thread = Thread(target=self._launch, args=(task_id, task))
        task_thread.start()

    def _launch(self, task_id, task: Task):
        logger.info("Starting " + task.name())
        try:
            task.run()
        except Exception as ex:
            logger.error("Fail when running " + task.name())
            logger.error(ex)
            task.when_failed()
            traceback.print_tb(ex.__traceback__)
        finally:
            self.is_launched[task_id] = False
            logger.info("Finished " + task.name())
