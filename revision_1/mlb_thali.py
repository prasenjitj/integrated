"""This script converts mlb raw data to thali format and dedupes it as well.

It takes two arguments raw input data file and thali converted output file.
usage : $ python sportsRoster.py mlb_raw.tsv mlb_thali.py.
"""
from collections import defaultdict
from collections import OrderedDict
import re


def mlb_thali(str1, str2):
  """converts raw data to thali format for mlb leagues."""
  print 'mlb_thali script invoked'
  f = open(str1, 'r')

  data = f.read().strip()
  data = data.split('\n')
  header = data[0]
  # d={}
  # d1={}
  dd = defaultdict(list)
  # print data
  list1 = []
  list2 = []
  new_tags = set()
  mapping = {'Signed as Free Agent': 'SPLGROSTMlb',
             'Number Change': 'SPLGROUSMlb',
             'Designated for Assignment': 'SPLGROSTMlb',
             'Trade': 'SPLGROSTMlb',
             'Released': 'SPLGROSTMlb',
             'Claimed Off Waivers': 'SPLGROSTMlb',
             'Selected': 'SPLGROSTMlb',
             'Outrighted': 'SPLGROSTMlb',
             'Status Change': 'SPLGROUSMlbMar14',
             'Signed': 'SPLGROSTMlb',
             'Assigned': 'SPLGROSTMlb',
             'Optioned': 'SPLGROSTMlb',
             'Retired': 'SPLGROSTMlb',
             'Returned': 'SPLGROSTMlb',
             'Recalled': 'SPLGROSTMlb',
             'Loan': 'SPLGROSTMlb'}
  key = header.split('\t')
  # print key

  for i in range(1, len(data)):
    value = data[i]
    value = value.split('\t')

    if value[3]:
      pass
    else:
      # print 'test'
      value = ''

    # print value
    new = OrderedDict(zip(key, value))
    # print new

    if new:
      list1.append(new)
    else:
      # print 'dictionary is empty'
      pass

  record = list1
  # print record

  for i, j in enumerate(record):
    match1 = re.findall(r'signed\s*free\s*agent', j['note'])
    match1 = ''.join(match1)
    match2 = re.findall(r'to\s*spring\s*training', j['note'])
    match2 = ''.join(match2)
    if match1 == 'signed free agent':
      pass
    elif match2 == 'to spring training':
      j['type'] = 'Spring Training'

    task_name = j['note']
    j['task_name'] = task_name

    if j['type'] not in mapping.keys():
      new_tags.add(j['type'])

    tag = j['type']
    j['tag'] = tag

    for k, v in mapping.items():
      if j['tag'] == k:
        tag = v
        j['tag'] = tag
    # print j['tag']

    ex_id = (j['transaction_id'] + '#' + j['player'] + '#' + j['team']+'#'
             + j['type'])

    # print  ex_id
    j['trans_date'] = re.sub(r'T.*', '', j['trans_date'])
    date = j['trans_date']
    matchobj = re.match(r'2016-(.*?)-.*', date)
    month = matchobj.group(1)
    month = int(month)
    for i in range(1, 13):
      if month == i:
        j['url'] = (
            'http://www.mlb.com/mlb/transactions/#month=' + str(i) +
            '&year=2016')

    description = (
        '*Find or create each transaction and curate as per '
        'guidelines* Player Name: ' + j['player'] + ' # Team Name: '
        + j['team'] + ' # Type: ' + j['type'] + ' # Transaction: ' + j
        ['note'] + ' # Transaction date: ' + j['trans_date'])
    task_type = '/common/topic'
    j['description'] = description

    j['external_id'] = ex_id

    j['task_type'] = task_type

    # print j['trans_date']

    if j['type'] == 'Spring Training':
      j.clear()
      # print 'deleted'
    if j:
      list2.append(j)
    else:
      pass
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
        'task_type', 'task_name', 'url', 'description', 'tag', 'external_id']
    final_dict = OrderedDict([(a, dd2[a]) for a in wanted_keys if a in dd2])
    # print final_dict['URL']

    f1.write('\t'.join(final_dict.keys()) + '\n')
    for b in zip(*final_dict.values()):
      f1.write('\t'.join(b) + '\n')
