"""This script converts nba raw data to thali format.

It takes two arguments raw input data file and thali converted output file.
usage : $ python sportsRoster.py nba_raw.tsv nba_thali.py.
"""
from collections import defaultdict
from collections import OrderedDict
import re
KEY_MAP = {'Signing': 'SPLGROSTNba',
           'Trade': 'SPLGROSTNba',
           'Waive': 'SPLGROSTNba',
           'AwardedOnWaivers': 'SPLGROSTNba'}


def nba_thali(infile, outfile):
  """converts raw data to thali format for mlb leagues."""
  print 'nba_thali script invoked'

  fread = open(infile, 'r')

  data = fread.read().strip()
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
    # print value
    new_dic = OrderedDict(zip(key, value))
    # print new
    list1.append(new_dic)

  record = list1
  # print record

  for row_j in record:
    tag = row_j['GroupSort']
    tag = re.sub(r'\s\d.*', '', tag)
    row_j['tag'] = tag

    if row_j['tag'] not in KEY_MAP.keys():
      new_tags.add(row_j['tag'])
    for k, v in KEY_MAP.items():
      if row_j['tag'] == k:
        tag = v
        row_j['tag'] = tag
    date = row_j['Transaction_Date']
    date = re.sub(r'-', '', date)
    row_j['date'] = date
    ex_id_old = row_j['date'] + '#' + row_j['GroupSort'] + '#' + row_j[
        'Team_ID'] + '#' + row_j['Transaction_Description']
    ex_id_new = row_j['date'] + '#' + row_j['GroupSort'] + '#' + row_j[
        'Transaction_Description']
    ex_id_new = re.sub(r'\s#', '#', ex_id_new)
    # print  ex_id_new
    row_j['url'] = 'http://stats.nba.com/transactions'
    description = ('*Find or create each transaction and '
                   'curate as per guidelines* Transaction_Description: ')
    description += row_j['Transaction_Description'] + ' # Transaction_Date: '
    description += row_j['Transaction_Date'] + ' # URL: ' + row_j['url']
    task_type = '/common/topic'
    row_j['description'] = description
    row_j['external_id'] = ex_id_new
    row_j['external_id_old'] = ex_id_old
    row_j['task_type'] = task_type

    task_name = row_j['Transaction_Description']
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

    wanted_keys = [
        'task_type', 'task_name', 'url', 'description', 'tag', 'external_id',
        'external_id_old']
    final_dict = OrderedDict([(a, dic2[a]) for a in wanted_keys if a in dic2])
    # print final_dict

    fwrite.write('\t'.join(final_dict.keys()) + '\n')
    for b in zip(*final_dict.values()):
      fwrite.write('\t'.join(b) + '\n')
