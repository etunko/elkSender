# from pprint import pprint
from mailWorker import mongoReq
from mailWorker import mailCondition
from mailWorker import smtpSend
import copy
import datetime


def dictValues(var, logger, local_var):
    for key, value in var.items():
        if type(var[key]) is not str:
            dictValues(var[key], logger, local_var)
        else:
            for k in local_var.keys():
                if k == var[key]:
                    var[key] = local_var[k]
    return(var)


def handler(event, logger):
    local_var = {"<!'start_time'!>": event['start_time'], "<!'end_time'!>": event['end_time']}
    result_final = ['null' for x in range(maxChain(event['logic']['queries'], logger))]
    for query in event['logic']['queries']:
        q = copy.deepcopy(query['query'])
        result_var = {}
        for res_var in query['result']:
            result_var.update({res_var: ''})
        q = dictValues(q, logger, local_var)
# ###########################
# ####DELETE###DELETE########
# ###########################
        q.update({'@timestamp': {'$gte': datetime.datetime(2017, 7, 1, 0, 0), '$lt': datetime.datetime(2017, 8, 1, 0, 0)}})
# ###########################
# ####DELETE###DELETE########
# ###########################
        mongoReq.resultMongo(q, result_final, query['result'], query['in_chain'], query['command'])
    mailResult = mailCondition.condition(result_final, event['logic']['condition_output'])
    smtpSend.sendler(mailResult, logger, event['mail'])
#    print(next(mailResult))
#    print(next(a))
#    pprint(result_final)


def maxChain(queries, logger):
    chains = 0
    for i in range(len(queries)):
        if int(queries[i]['in_chain']) > int(chains):
            chains = int(queries[i]['in_chain'])
        if i > 0:
            if int(queries[i]['in_chain']) < int(queries[i-1]['in_chain']):
                logger.error("Chain is not ordered\n" + str(queries))
    return(chains+1)
