from collections import defaultdict
from collections import OrderedDict

def thali(str1,str2):
    f=open(str1,'r')

    data=f.read().strip()
    data=data.split('\n')
    header=data[0]
    #d={}
    #d1={}
    dd=defaultdict(list)
    #print data
    list1=[]
    list2=[]
    #values=[]

    key=header.split('\t')
    #print key
    #
    for i in range(1,len(data)):
        value=data[i]
        value=value.split('\t')
        if value[12] == '':
            #print 'test'
            value = ''
        #print value[3]
        #print value
        new=OrderedDict(zip(key,value))
        #print new

        if new:
            list1.append(new)
        else:
            print 'dictionary is empty'
        
    record= list1
    #print record


    for j in record:
        ex_id = j['transaction_id']+'#'+j['player']+'#'+j['team']+'#'+j['type']
        #print  ex_id
        description = '*Find or create each transaction and curate as per guidelines* Player Name: '+j['player']+' # Team Name: '+j['team']+' # Type: '+j['type']+' # Transaction: '+j['note']+' # Transaction date: '+j['trans_date']
        task_type = '/common/topic'
        j['Description']=description
        j['external_id']=ex_id
        j['Task_Type'] = task_type
        list2.append(j)
    #print list2

    for x in list2:
        tag=x.keys()
        tag=tuple(tag)
    #print tag

    dd2=defaultdict(list)

    with open (str2,'w') as f1:
        #f1.write('\t'.join(tag)+'\n')
        for row in list2:
            for k in tag:
                
                if k not in row.keys():
                    dd[k]=''
                    #print 'false'
                else:
                    dd[k]=row[k]
                    #print 'true', row[k]
                dd2[k].append(dd[k])

        wanted_keys = ['player','type','Task_Type','URL','Description','external_id','note']
        final_dict=dict([(a,dd2[a]) for a in wanted_keys if a in dd2])
        #print final_dict

        f1.write('\t'.join(final_dict.keys())+'\n')
        for b in zip(*final_dict.values()):
            f1.write('\t'.join(b)+'\n')