# nvdashboard version 2
import os
import sys
import re
import time
import datetime
from datetime import datetime as dt
import copy


class nvdashboard2:
    def __init__(self, conf={}):
        # Information to be acquired when initialized
        self.status = {}
        self.status['cwd'] = os.getcwd()
        self.status['platform'] = sys.platform
        self.status['start'] = dt.now()
        # Read conf when instantiating
        if len(conf) == 0:
            print(' conf is empty ')
            return
        self.conf = conf

        # Default member variable name:
        # conf,status,result,pers,error_msg,items
        # Save value with each run
        self.result = {}
        # Use pers if you want to save the value across executions
        self.pers = {}
        # error_msg
        self.error_msg = []
        # date time when instantiating
        print(self.status['start'].strftime('%Y-%m-%d %H:%M:%S'))

    # Useful function for List comprehension
    def re(self, tg, xlist):
        return([x for x in xlist if re.search(tg, x)])

    # sleep

    def sleep(self, args=[]):
        if len(args) == 0:
            time.sleep(1)
        else:
            time.sleep(int(args[0]))

    # Set items
    def set_items(self, noun="", verb="", override={}):
        self.items = {}
        items = {}
        if noun not in self.conf['nouns'].keys():
            print(" noun is not in nouns ")
            self.items = {}
            return False
        else:
            if noun != "":
                items = copy.deepcopy(self.conf['nouns'][noun])
        if verb not in self.conf['verbs'].keys():
            print(" verb not in verbs ")
            self.items = {}
            return False
        else:
            if verb != "":
                # set verb not in noun
                for k in self.conf['verbs'][verb].keys():
                    if k not in items.keys():
                        items[k] = copy.deepcopy(self.conf['verbs'][verb][k])

        def set_common(c, i):
            if type(i) == dict:
                for k in i.keys():
                    if (type(i[k]) == dict and
                       len(i[k]) == 1 and
                       list(i[k].keys())[0] == 'xxx_common_xxx'):
                        i[k] = copy.deepcopy(c[k][i[k]['xxx_common_xxx']])
                    if type(i[k]) == dict and len(i[k]) > 0:
                        i[k] = set_common(c, i[k])
                return(i)
            else:
                return(i)
        items = set_common(self.conf['commons'], items)
        # set global not in verb,noun
        for k in self.conf['global']:
            if k not in items.keys():
                items[k] = copy.deepcopy(self.conf['global'][k])

        # override function
        def ride(o, i):
            for k in o:
                if (k not in i.keys() or
                   type(o[k]) != dict or
                   type(i[k]) != dict):
                    i[k] = o[k]
                else:
                    i[k] = ride(o[k], i[k])
            return(i)
        if len(override) > 0:
            items = ride(override, items)
        # set noun,verb if not in items.keys()
        if 'noun' not in items.keys():
            items['noun'] = noun
        if 'verb' not in items.keys():
            items['verb'] = verb
        self.items = copy.deepcopy(items)
        return True

    def do(self, noun="", verb="", do_flag=False, override={}):
        self.noun = noun
        if len(self.error_msg) > 0:
            print('...Error')
            for one in self.error_msg:
                print(one)
            return False

        # set items
        i_tf = self.set_items(noun, verb, override)
        if not i_tf:
            return False
        if type(do_flag) != bool:
            do_flag = False

        # Do when do_flag is True
        if do_flag:
            for one in self.items['do']:
                xlist = one.split(',')
                if len(xlist) > 1:
                    eval('self.' + xlist[0] + '(xlist[1:])')
                else:
                    eval('self.' + xlist[0] + '()')
            return True
        else:
            print()
            print(' dry run ')
            print(' ds.items  ')
            print()
            return True
        return True

    # Execute if there is an argument for test or exec in items
    def test(self, script=""):
        if script != "":
            exec(script)
        try:
            if "exec" in self.items.keys():
                exec(self.items['exec'])
        except:
            pass
