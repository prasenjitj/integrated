"""This script converts mlb raw data to thali format and dedupes it as well.

It takes two arguments raw input data file and thali converted output file.
usage : $ python sportsRoster.py mlb_raw.tsv mlb_thali.py.
"""
from collections import defaultdict
from collections import OrderedDict
import re
KEY_MAP = {'Signed as Free Agent': 'SPLGROSTMlb',
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


def mlb_thali(infile, outfile):
  """converts raw data to thali format for mlb leagues."""
  print 'mlb_thali script invoked'
  fread = open(infile, 'r')

  data = fread.read().strip()
  data = data.split('\n')
  header = data[0]
  # d={}
  # d1={}
  dic1 = defaultdict(list)
  # print data
  list1 = []
  list2 = []
  new_tags = set()
  key = header.split('\t')
  # print key

  for row_i in range(1, len(data)):
    value = data[row_i]
    value = value.split('\t')

    if value[3]:
      pass
    else:
      # print 'test'
      value = ''

    # print value
    new_dic = OrderedDict(zip(key, value))
    # print new

    if new_dic:
      list1.append(new_dic)
    else:
      # print 'dictionary is empty'
      pass

  record = list1
  # print record

  for row_i, row_j in enumerate(record):
    match1 = re.findall(r'signed\s*free\s*agent', row_j['note'])
    match1 = ''.join(match1)
    match2 = re.findall(r'to\s*spring\s*training', row_j['note'])
    match2 = ''.join(match2)
    if match1 == 'signed free agent':
      pass
    elif match2 == 'to spring training':
      row_j['type'] = 'Spring Training'

    task_name = row_j['note']
    row_j['task_name'] = task_name

    if row_j['type'] not in KEY_MAP.keys():
      new_tags.add(row_j['type'])

    tag = row_j['type']
    row_j['tag'] = tag

    for row_k, row_v in KEY_MAP.items():
      if row_j['tag'] == row_k:
        tag = row_v
        row_j['tag'] = tag
    # print j['tag']

    ex_id = (row_j['transaction_id'] + '#' + row_j['player'] + '#' +
             row_j['team']+'#' + row_j['type'])

    # print  ex_id
    row_j['trans_date'] = re.sub(r'T.*', '', row_j['trans_date'])
    date = row_j['trans_date']
    matchobj = re.match(r'2016-(.*?)-.*', date)
    month = matchobj.group(1)
    month = int(month)
    for i in range(1, 13):
      if month == i:
        row_j['url'] = (
            'http://www.mlb.com/mlb/transactions/#month=' + str(i) +
            '&year=2016')

    description = (
        '*Find or create each transaction and curate as per '
        'guidelines* Player Name: ' + row_j['player'] + ' # Team Name: '
        + row_j['team'] + ' # Type: ' + row_j['type'] + ' # Transaction: ' +
        row_j['note'] + ' # Transaction date: ' + row_j['trans_date'])
    task_type = '/common/topic'
    row_j['description'] = description

    row_j['external_id'] = ex_id

    row_j['task_type'] = task_type

    # print j['trans_date']

    if row_j['type'] == 'Spring Training':
      row_j.clear()
      # print 'deleted'
    if row_j:
      list2.append(row_j)
    else:
      pass
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

    wanted_keys = [
        'task_type', 'task_name', 'url', 'description', 'tag', 'external_id']
    final_dict = OrderedDict([(a, dic2[a]) for a in wanted_keys if a in dic2])
    # print final_dict['URL']

    fwrite.write('\t'.join(final_dict.keys()) + '\n')
    for b in zip(*final_dict.values()):
      fwrite.write('\t'.join(b) + '\n')
