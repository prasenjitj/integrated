import re
import datetime
from collections import defaultdict
from collections import OrderedDict

def nhlThali(str1,str2):
	f=open(str1,'r')

	data=f.read().strip()
	data=data.split('\n')
	header=data[0]
	d={}
	d1={}
	dd=defaultdict(list)
	#print data
	list1=[]
	list2=[]
	values=[]
	new_tags = set()

	mapping = {
				'Agreed':'SPLGROSTNhl',
				'Assigned':'SPLGROSTNhl',
				'Lifted':'SPLGROUSNhl',
				'Recalled':'SPLGROSTNhl',
				'Reassigned':'SPLGROSTNhl',
				'Signed':'SPLGROSTNhl'
				}
	key=header.split('\t')
	#print key
	#
	for i in range(1,len(data)):
		value=data[i]
		value=value.split('\t')
		#modify url
		new_url=value[0]
		new_url=re.sub(r'\s*REC#\s* ','#',new_url)
		value[0]=new_url

		

		#print value[0]
		new=OrderedDict(zip(key,value))
		#print new
		list1.append(new)



	record= list1
	#print record

	for j in record:
		#modify date
		new_date = j['Date']
		new_date=datetime.datetime.strptime(new_date,'%B %d, %Y')
		new_date= datetime.datetime.strftime(new_date,'%Y-%m-%d')
		j['date']=new_date
		#print new_date
		if j['tag'] not in mapping.keys():
			new_tags.add(j['tag'])

		for k, v in mapping.items():
		    if j['tag'] == k:
		        tag=v
		        j['tag'] = tag
		ex_id = j['url']+'#'+j['Transaction']
		#print  ex_id
		description = '*Find or create each transaction and curate as per guidelines* Transaction: '+j['Transaction']+' # Date: '+j['date']+' # URL: '+j['url']
		task_type = '/common/topic'
		j['description']=description
		j['external_id']=ex_id
		j['task_type'] = task_type
		task_name = j['Transaction']
		j['task_name'] = task_name
		list2.append(j)
		  
	#print list2
	print 'New Tag found contact Daiel',new_tags


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

		'''		
		#print dd2
		f1.write('\t'.join(dd2.keys())+'\n')
		for v in zip(*dd2.values()):	
			#print '\t'.join(v),'\n'		
			f1.write('\t'.join(v)+'\n')	
		'''	

		wanted_keys = ['task_type','task_name','url','description','tag','external_id']
		final_dict=OrderedDict([(a,dd2[a]) for a in wanted_keys if a in dd2])
		#print final_dict

		f1.write('\t'.join(final_dict.keys())+'\n')
		for b in zip(*final_dict.values()):
			f1.write('\t'.join(b)+'\n')