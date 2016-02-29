import re
import sys
from collections import defaultdict
from collections import OrderedDict

#infile =sys.argv[1]
#outfile =sys.argv[2]
print 'soccer thali script invoked'

f=open('1.tsv','r')

data=f.read().strip()
data=data.split('\n')
header=data[0]
dd=defaultdict(list)
#print data
list1=[]
list2=[]

key=header.split('\t')
#print key
#
for i in range(1,len(data)):
    value=data[i]
    value=value.split('\t')
    #print value
    if value[2] != '2016':
    	value = ''
    new=OrderedDict(zip(key,value))
    #print new
    if new:

        list1.append(new)
    else:
        pass
        #print 'dictionary is empty'
record= list1

#print record[-1]

for j in record:
	url = j['url']
	
	url = re.sub(r'\s*REC#\s*',"/",url)
	url = re.sub(r'\\','/',url)
	
	#print type(url)
	j['URL'] = url
	description = '*Find or create each transaction and curate as per guidelines* Player Name: '+j['Player_name']+' # From Team: '+j['From_Team']+' # To Team: '+j['To_Team']+' # Transaction Date: '+j['Date']+' # URL: '+j['URL']
	task_type = '/soccer/football_player'
	j['Description']=description
	#j['external_id']=ex_id
	j['Task_Type'] = task_type
	list2.append(j)

#print list2


for x in list2:
	tag=x.keys()
	tag=tuple(tag)
#print tag

dd2=defaultdict(list)

with open ('2.tsv','w') as f1:
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
	#print dd2
	'''		
	#print dd2
	f1.write('\t'.join(dd2.keys())+'\n')
	for v in zip(*dd2.values()):	
		#print '\t'.join(v),'\n'		
		f1.write('\t'.join(v)+'\n')	
	'''	

	wanted_keys = ['URL','Task_Name','Task_Type','External_id','Description']
	final_dict=OrderedDict([(a,dd2[a]) for a in wanted_keys if a in dd2])
	print final_dict.values()

	f1.write('\t'.join(final_dict.keys())+'\n')
	for b in zip(*final_dict.values()):
		f1.write('\t'.join(b)+'\n')