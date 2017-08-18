import scheduleConf
from logger import logger, importantLog
from pprint import pformat
from elkScheduler import elkCron
import queue
from mailWorker import mailWorker
import os


print(os.getpid())


class main():
    def __init__(self, logger, configLocate):
        self.logger = logger
        self.confogLocate = configLocate
        self.startApp()
        self.schConfig

    def startApp(self):
        importantLog(logger.info, 'Starting App...')
        schConfObj = scheduleConf.schedulerConf(self.logger, self.confogLocate)
        self.schConfig = schConfObj.config
        logger.debug('Received next congiguration : \n' + pformat(self.schConfig))
        logger.debug("Creating queue ")
        self.q = queue.Queue()
        logger.debug("Creating cron schedule")
        self.cron = elkCron.mailScheduler(elkCron.elkDefaulFunc, self.schConfig, self.q)
        logger.debug("Starting cron....")
        self.cron.start()
        logger.debug("Creating threading workers ")
        self.workers = mailWorker(config_url='', q=self.q, logger=self.logger)
        self.workers.startThreads()


myApp = main(logger, 'C:\git\elk_sender\Scheduler_Config')

# Тестируем
from importlib import reload
from mailWorker import mailSender


def myReload():
    mailSender = reload(mailSender)
#myApp.cron.pause()
