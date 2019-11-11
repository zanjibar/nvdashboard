# nvdashboard version 2 
import os,sys,re,json,codecs,time,string
import datetime
import copy
from datetime import datetime as dt

class nvdashboard2:
    def __init__(self,conf={}):
        
        # Information to be acquired when initialized
        self.status= {}
        self.status['cwd'] = os.getcwd()
        self.status['platform'] = sys.platform
        self.status['start'] = dt.now()
        
        # Read conf when instantiating  
        if len(conf) == 0:
            print(' conf is empty ')
            return
        self.conf = conf

        # Default member variable name: conf,status,result,pers,error_msg,items 

        # Save value with each run

        self.result = {}
        
        # Use pers if you want to save the value across executions
        self.pers = {}
        
        # error_msg 
        self.error_msg = []

        # date time when instantiating
        print(self.status['start'].strftime('%Y-%m-%d %H:%M:%S'))

    # Useful function for List comprehension 
    def re(self,tg,xlist):
        return([x for x in xlist if re.search(tg,x)])
    
    # sleep 
    def sleep(self,args=[]):
        if len(args) == 0:
            time.sleep(1)
        else:
            time.sleep(int(args[0]))

            

    # 項目(items) を 設定する
    def set_items(self,noun="",verb="",override = {}):
        # self.items を初期化する
        self.items = {}
        items = {}

        if  noun not in self.conf['nouns'].keys() :
            print(" ★ 名詞 ( " + noun + " ) の指定が間違っています。 ★ ")
            print('名詞一覧')
            print(list(self.conf['nouns'].keys()))
            print('動詞一覧')
            print(list(self.conf['verbs'].keys()))
            self.items = {}
            return False
        else:
            # items に、名詞(noun)をcopy 設定
            if noun != "":
                items = copy.deepcopy(self.conf['nouns'][noun])
        
        
        if  verb not in self.conf['verbs'].keys() :
            print(" ★ 動詞(verb) の指定が間違っています。 ★ ")
            print('動詞一覧')
            print(list(self.conf['verbs'].keys()))
            print('名詞の内容 ( ' + noun + ' )')
            print(self.conf['nouns'][noun])
            self.items = {}
            return False
        else:
            if verb !="":
                # 動詞(verb) を適用　名詞(noun)にない項目を設定
                for k in self.conf['verbs'][verb].keys():
                    if k not in items.keys():
                        items[k] = copy.deepcopy(self.conf['verbs'][verb][k])
                        


        def set_common(c,i):
            if type(i) == dict :
                for k in i.keys():
                    if type(i[k])==dict and len(i[k])==1 and list(i[k].keys())[0]=='xxx_common_xxx':
                        i[k] = copy.deepcopy(c[k][i[k]['xxx_common_xxx']])
                    if type(i[k])==dict and len(i[k]) > 0:
                        i[k] = set_common(c,i[k])
                return(i)
            else:
                return(i)
                
        items = set_common(self.conf['commons'],items)

                                                                              
        #未定義の項目が全体(global)にあったら設定
        for k in self.conf['global']:
            if k not in items.keys():
                items[k] = copy.deepcopy(self.conf['global'][k])


        # 上書きの設定
        def ride(o,i):
            for k in o:
                if k not in i.keys() or type(o[k]) !=dict or type(i[k]) !=dict:
                    i[k] = o[k]
                else:
                    i[k] = ride(o[k],i[k])
            return(i)


        if len(override) > 0:
            items = ride(override,items)
        
     
        
        # noun,verb がitem に設定されていないかったら、設定する
        if 'noun' not in items.keys():
            items['noun'] = noun
         
        if 'verb' not in items.keys():
            items['verb'] = verb
            
        self.items = copy.deepcopy(items)
        return True

    def do(self,noun="",verb="",do_flag = False,override = {}):
        self.noun = noun
        if len(self.error_msg) > 0 :
            print('エラーメッセージがあります。 ...Error')
            for one in self.error_msg:
                print(one)
            return False

        # items を設定する
        i_tf = self.set_items(noun,verb,override)
        
        # items 作成でエラーになった場合は、False を戻す
        if not i_tf:
            return False

        
        if type(do_flag) !=bool:
            do_flag = False

        # noun,verb の次の３番目の変数が、真の時に、do の内容を実行する
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


    # test 用 引数、もしくは、items に exec があったら実行する
    def test(self,script=""):
        if script != "":
            exec(script)
        try:
            if "exec" in self.items.keys():
                exec(self.items['exec'])
        except:
            pass


