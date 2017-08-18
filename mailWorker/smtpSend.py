from pprint import pformat


def sendler(mailResult, logger, mailInf):
    print(pformat(mailInf))
    print(next(mailResult))
