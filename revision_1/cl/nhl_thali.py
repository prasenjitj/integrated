"""This script converts nhl raw data to thali format.

It takes two arguments raw input data file and thali converted output file.
usage : $ python sportsRoster.py nhl_raw.tsv nhl_thali.py.
"""
from collections import defaultdict
from collections import OrderedDict
import datetime
import re
KEY_MAP = {'Agreed': 'SPLGROSTNhl',
           'Assigned': 'SPLGROSTNhl',
           'Lifted': 'SPLGROUSNhl',
           'Recalled': 'SPLGROSTNhl',
           'Reassigned': 'SPLGROSTNhl',
           'Signed': 'SPLGROSTNhl',
           'Announced': 'SPLGROUSNflMar14',
           'Activated': 'SPLGROUSNhl',
           'Placed': 'SPLGROUSNhl',
           'Reinstated': 'SPLGROUSNhl',
           'Reasigned': 'SPLGROSTNhl',
           'Called': 'SPLGROSTNhl',
           'Fired': 'SPLGROSTNhl'}


def trim(ext_id):
  if len(ext_id) >= 200:
    new_id = ext_id[0:199]
    return new_id
  else:
    return ext_id


def nhl_thali(infile, outfile):
  """converts raw data to thali format for nhl leagues."""
  print 'nhl_thali script invoked'
  fopen = open(infile, 'r')

  data = fopen.read().strip()
  data = data.split('\n')
  header = data[0]
  dic1 = defaultdict(list)
  # print data
  list1 = []
  list2 = []
  new_tags = set()

  key = header.split('\t')
  # print key
  #
  for row_i in range(1, len(data)):
    value = data[row_i]
    value = value.split('\t')
    # modify url
    new_url = value[0]
    new_url = re.sub(r'\s*REC#\s* ', '#', new_url)
    value[0] = new_url

    # print value[0]
    new_dic = OrderedDict(zip(key, value))
    # print new
    list1.append(new_dic)

  record = list1
  # print record

  for row_j in record:
    # modify date
    new_date = row_j['Date']
    new_date = datetime.datetime.strptime(new_date, '%B %d, %Y')
    new_date = datetime.datetime.strftime(new_date, '%Y-%m-%d')
    row_j['date'] = new_date
    new_date = re.sub(r'-', '', new_date)

    if row_j['tag'] not in KEY_MAP.keys():
      new_tags.add(row_j['tag'])

    for k, v in KEY_MAP.items():
      if row_j['tag'] == k:
        tag = v
        row_j['tag'] = tag
    ex_id = row_j['url']
    ex_id = re.sub(
        r'http://espn.go.com/nhl/transactions', 'transactions', ex_id)
    # print  ex_id
    description = (
        '*Find or create each transaction and curate as per guidelines* '
        'Transaction: ' + row_j['Transaction'] + ' # Date: ' +
        row_j['date'] + ' # URL: ' + row_j['url'])
    new_exid = trim(ex_id)
    # print new_exid
    row_j['external_id'] = new_exid
    task_type = '/common/topic'
    row_j['description'] = description
    row_j['external_id_old'] = ex_id
    row_j['task_type'] = task_type
    task_name = row_j['Transaction']
    row_j['task_name'] = task_name
    list2.append(row_j)

  # print list2
  print 'New Tag found contact Daiel', new_tags

  for row_x in list2:
    tag = row_x.keys()
    tag = tuple(tag)
  # print tag

  dic2 = defaultdict(list)

  with open(outfile, 'w') as fwrite:
    # f1.write('\t'.join(tag)+'\n')
    for row in list2:
      for row_k in tag:

        if row_k not in row.keys():
          dic1[row_k] = ''
          # print 'false'
        else:
          dic1[row_k] = row[row_k]
          # print 'true', row[k]
        dic2[row_k].append(dic1[row_k])

    wanted_keys = ['task_type', 'task_name', 'url', 'description',
                   'tag', 'external_id_old', 'external_id']
    final_dict = OrderedDict([(a, dic2[a]) for a in wanted_keys if a in dic2])
    # print final_dict

    fwrite.write('\t'.join(final_dict.keys()) + '\n')
    for b in zip(*final_dict.values()):
      fwrite.write('\t'.join(b) + '\n')
      