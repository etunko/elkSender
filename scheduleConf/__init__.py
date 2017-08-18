from os import listdir
from os.path import isfile, join
import json


class schedulerConf():
    def __init__(self, logger, fileLocate):
        logger.debug("Init schedulerConf, directory - " + fileLocate)
        self.config = list()
        self.logger = logger
        self.fileLocate = fileLocate
        self.scheduleList()

    def getFiles(self):
        try:
            files = [join(self.fileLocate, f) for f in listdir(self.fileLocate) if isfile(join(self.fileLocate, f))]
            return(files)
        except OSError:
            self.logger.error('There are no directory ' + self.fileLocate)

    def scheduleList(self):
        for f in self.getFiles():
            with open(f) as data_file:
                self.config.extend(json.load(data_file)['events'])
