from time import sleep
import threading
from mailWorker import mailSender


class mailWorker():
    def __init__(self, config_url, q, logger):
        self.config_url = config_url
        self.q = q
        self.logger = logger
        self.sleep_worker = 5
        self.num_worker_threads = 2
        self.threads = []

    def worker(self):
        while True:
            if self.q.empty() is True:
                sleep(self.sleep_worker)
            else:
                event = self.q.get()
                self.logger.debug("Get message from"+str(event))
#                mailSender.handler(event, self.logger)
                self.q.task_done()

    def initThreads(self):
        for i in range(self.num_worker_threads):
            t = threading.Thread(target=self.worker)
            self.threads.append(t)

    def startThreads(self):
        self.initThreads()
        for t in self.threads:
            t.start()
