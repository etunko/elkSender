from pymongo import MongoClient
import re


def find(query):
#    uri = 'mongodb://logstash:depo2012@172.30.161.20:19332/'
    client = MongoClient('172.30.161.20', 19332)
    db = client['elk']
    db.authenticate('logstash', 'depo2012')
    data = db['data']
    res = data.find(query)
    return(res)


def preparResult(result, field_res):
    res = {}
    pattern = re.compile("<!\$'([\w,-,_].+)'\$!>")
    for field in field_res:
        if field == "<!'count'!>":
            res.update({"<!'count'!>": result.count()})
        else:
            res.update({pattern.findall(field)[0]: []})

    for col in result:
        for field in field_res:
            try:
                if pattern.findall(field)[0] in col.keys():
                    res[pattern.findall(field)[0]].append(col[pattern.findall(field)[0]])
            except IndexError:
                pass
    with open('exp.txt', 'a+') as f:
        f.write(str(res))
    return(res)


def resultMongo(query, result_final, field_res, in_chain, command):
    if command == 'find':
        result = find(query)
    result_dict = preparResult(result, field_res)
    result_final[int(in_chain)] = result_dict
