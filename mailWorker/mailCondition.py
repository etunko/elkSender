from pprint import pprint, pformat
import copy
from logger import logger


def comparePreparer(cond, result):
    def var(el):
        if el.get("in_chain"):
            a = result[el["in_chain"]][el["variable"]]
#            print("A =" + str(a))
        elif el.get("constant") or el.get("constant") == 0:
            a = el["constant"]
#            print("B =" + str(a))
        return(a)
    def comp(A, B, cmd, result):
        def useStr(A, B, cmd, result):
            if cmd == '==':
                boolean = str(A) == (B)
            elif cmd == ('!=' or '<>'):
                boolean = str(A) != (B)
            elif cmd == ('>' or '<' or '>=' or '<='):
                try:
                    A = int(A)
                    B = int(A)
                    if cmd == '>':
                        boolean == A > B
                    elif cmd == '>=':
                        boolean == A >= B
                    elif cmd == '<':
                        boolean == A < B
                    elif cmd == '<=':
                        boolean == A <= B
                except TypeError:
                    raise
            return(boolean, result)
        def useStrList(A, B, cmd, result):
            i = 0
            while (i <= len(result)-1) and len(result) != 0:
                if cmd == '==':
                    if result[i] == B:
                        i += 1
                    else:
                        result.pop(i)
                elif cmd == ('!=' or '<>'):
                    if result[i] == B:
                        result.pop(i)
                    else:
                        i += 1
            if len(result) > 0:
                boolean = True
            else:
                boolean = True
            return(boolean, result)
#        print('-----------------------------')
#        print(str(type(A)) + '  ' + str(A))
#        print(str(type(B)) + '  ' + str(B))
        if (type(A) is (int or str) and type(B) is (int or str)) or (type(A) is list and type(B) is list):
            boolean, result = useStr(A, B, cmd, result)
        elif (((type(A) is int or type(A) is str) and type(B) is list) or ((type(B) is int or type(B) is str) and type(A) is list)):
            if type(A) is list:
                boolean, result = useStrList(A, B, cmd, result)
            else:
                boolean, result = useStrList(B, A, cmd, result)
#        print('-----------------------------')
        return(boolean, result)
    boolean, result = comp(var(cond["A"]), var(cond["B"]), cond['command'], result)
    return(boolean, result)


def condHelper(cond, result):
    def compare(bool_result, operators):
        def compareOper(A, B, op):
            if op == 'and':
                return(A and B)
            elif op == 'or':
                return(A or B)
        if len(bool_result) >= 2:
            boolean = compareOper(bool_result[0], bool_result[1], operators[0])
        elif len(bool_result) == 1:
            boolean = bool_result[0]
        elif len(bool_result) == 0:
            boolean = True
        else:
            for i in range(2, len(bool_result)-1):
                boolean = compareOper(boolean, bool_result[i], operators[i-1])
        return(boolean)
    bool_result = []
    for i in range(0, len(cond), 2):
        if type(cond[i]) is list:
            b_res, result = condHelper(cond[i], result)
        elif type(cond[i]) is dict:
            b_res, result = comparePreparer(cond[i], result)
        bool_result.append(b_res)
    operators = [cond[i] for i in range(1, len(cond), 2)]
    return(compare(bool_result, operators), result)


def condition(result, cond):
    res = copy.deepcopy(result)
    for c in cond:
        boolean, outres = condHelper(c['condition'], res)
        logger.debug('mailCondition.condition \n' +
                     str(boolean) + '\n' +
                     pformat(outres))
        if boolean is True:
            yield outres, c['output']
