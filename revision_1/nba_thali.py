"""This script converts nba raw data to thali format.

It takes two arguments raw input data file and thali converted output file.
usage : $ python sportsRoster.py nba_raw.tsv nba_thali.py.
"""
from collections import defaultdict
from collections import OrderedDict
import re


def nba_thali(str1, str2):
  """converts raw data to thali format for mlb leagues."""
  print 'nba_thali script invoked'

  f = open(str1, 'r')

  data = f.read().strip()
  data = data.split('\n')
  header = data[0]

  dd = defaultdict(list)
  # print data
  list1 = []
  list2 = []
  new_tags = set()
 

  mapping = {
      'Signing': 'SPLGROSTNba',
      'Trade': 'SPLGROSTNba',
      'Waive': 'SPLGROSTNba',
      'AwardedOnWaivers': 'SPLGROSTNba'
  }

  key = header.split('\t')
  # print key
  #
  for i in range(1, len(data)):
    value = data[i]
    value = value.split('\t')
    # print value
    new = OrderedDict(zip(key, value))
    # print new
    list1.append(new)

  record = list1
  # print record

  for j in record:
    tag = j['GroupSort']
    tag = re.sub(r'\s\d.*', '', tag)
    j['tag'] = tag

    if j['tag'] not in mapping.keys():
      new_tags.add(j['tag'])   
    for k, v in mapping.items():
      if j['tag'] == k:
        tag = v
        j['tag'] = tag
    date = j['Transaction_Date']
    date = re.sub(r'-', '', date)
    j['date'] = date
    ex_id_old = j[
        'date'] + '#' + j['GroupSort'] + '#' + j['Team_ID'] + '#' + j[
            'Transaction_Description']
    ex_id_new = j[
        'date'] + '#' + j['GroupSort'] + '#' + j['Transaction_Description']
    ex_id_new = re.sub(r'\s#', '#', ex_id_new)
    # print  ex_id_new
    j['url'] = 'http://stats.nba.com/transactions'
    description = ('*Find'
                   ' or '
                   'create'
                   ' '
                   'each'
                   ' '
                   'transaction'
                   ' and'
                   ' '
                   'curate'
                   ' as '
                   'per '
                   'guidelines*'
                   ' '
                   'Transaction_Description:'
                   ' ') + j[
                       'Transaction_Description'] + ' # Transaction_Date: ' + j[
                           'Transaction_Date'] + ' # URL: ' + j['url']
    task_type = '/common/topic'
    j['description'] = description
    j['external_id'] = ex_id_new
    j['external_id_old'] = ex_id_old
    j['task_type'] = task_type

    task_name = j['Transaction_Description']
    j['task_name'] = task_name
    list2.append(j)
  # print list2
  print 'New Tag found contact Daiel', new_tags

  for x in list2:
    tag = x.keys()
    tag = tuple(tag)
  # print tag

  dd2 = defaultdict(list)

  with open(str2, 'w') as f1:
    # f1.write('\t'.join(tag)+'\n')
    for row in list2:
      for k in tag:

        if k not in row.keys():
          dd[k] = ''
          # print 'false'
        else:
          dd[k] = row[k]
          # print 'true', row[k]
        dd2[k].append(dd[k])

    wanted_keys = [
        'task_type', 'task_name', 'url', 'description', 'tag', 'external_id',
        'external_id_old']
    final_dict = OrderedDict([(a, dd2[a]) for a in wanted_keys if a in dd2])
    # print final_dict

    f1.write('\t'.join(final_dict.keys()) + '\n')
    for b in zip(*final_dict.values()):
      f1.write('\t'.join(b) + '\n')
