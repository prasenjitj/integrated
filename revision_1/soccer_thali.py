"""This script converts soccer raw data to thali format and dedupes it.

It takes two arguments raw input data file and thali converted output file.
usage : $ python sportsRoster.py soccer_raw.tsv soccer_thali.py.
"""
from collections import defaultdict
from collections import OrderedDict
import re


def soccer_thali(str1, str2):
  """converts raw data to thali format for mlb leagues."""
  print 'soccer thali script invoked'

  f = open(str1, 'r')

  data = f.read().strip()
  data = data.split('\n')
  header = data[0]
  dd = defaultdict(list)
  list1 = []
  list2 = []

  code_mapper = {
      'A1': 'SPLGROSTAusFeb011',
      'AR1N': 'SPLGROSTArg',
      'AUS1': 'SPLGROSTAusFeb01',
      'BE1': 'SPLGROSTBel',
      'BRA1': 'SPLGROSTCam',
      'CAN': 'SPLGROSTCanFeb01',
      'DK1': 'SPLGROSTDan',
      'ES1': 'SPLGROSTLalFeb01',
      'FI1': 'SPLGROSTFin',
      'FR1': 'SPLGROSTLig',
      'GB1': 'SPLGROSTEngFeb012',
      'GB2': 'SPLGROSTEngFeb013',
      'GB3': 'SPLGROSTEngFeb011',
      'GB4': 'SPLGROSTEngFeb01',
      'GR1': 'SPLGROSTSupFeb011',
      'IR1': 'SPLGROSTRep',
      'IT1': 'SPLGROSTSerFeb012',
      'IT2': 'SPLGROSTIta',
      'KR1': 'SPLGROSTCro',
      'L1': 'SPLGROSTGerFeb01',
      'MEXA': 'SPLGROSTMex',
      'MLS1': 'SPLGROSTMls',
      'NL1': 'SPLGROSTDut',
      'PL1': 'SPLGROSTPol',
      'PO1': 'SPLGROSTPor',
      'RO1': 'SPLGROSTRom',
      'RSK1': 'SPLGROSTKor',
      'RU1': 'SPLGROSTRusFeb01',
      'SC1': 'SPLGROSTScoFeb01',
      'SER1': 'SPLGROSTSerFeb01',
      'SL1': 'SPLGROSTSloFeb01',
      'SLO1': 'SPLGROSTSlo',
      'TR1': 'SPLGROSTTur',
      'TS1': 'SPLGROSTCze',
      'UKR1': 'SPLGROSTUkr',
      'UNG1': 'SPLGROSTHun'
  }

  key = header.split('\t')

  for i in range(1, len(data)):
    value = data[i]
    value = value.split('\t')
    # print value
    if value[9] != '2016':
      value = ''
    new = OrderedDict(zip(key, value))
    # print new
    if new:

      list1.append(new)
    else:
      pass
      # print 'dictionary is empty'
  record = list1
  # print record
  for j in record:
    url = j['url']

    url = re.sub(r'\s*REC#\s*', '/', url)
    url = re.sub(r'\\', '/', url)
    url = re.sub(r'\d{4}-\d{2}-\d{2}', '', url)
    j['url'] = url
    for k, v in code_mapper.items():
      if j['code'] == k:
        tag = v
        j['tag'] = tag
    description = ('*Find or create each transaction and curate'
                   'as per guidelines* Player Name: ') + j['Player_name'] + (
                       ' # From Team: ') + j['From_Team'] + (' # To Team: ') + j[
                           'To_Team'] + ' # Transaction Date: ' + j[
                               'Date'] + ' # URL: ' + j['url']
    task_type = '/soccer/football_player'
    j['description'] = description
    j['Task_Type'] = task_type
    list2.append(j)
  # print list2  

  for x in list2:
    tag = x.keys()
    tag = tuple(tag)

  dd2 = defaultdict(list)

  with open(str2, 'w') as f1:
    for row in list2:
      for k in tag:
        if k not in row.keys():
          dd[k] = ''
        else:
          dd[k] = row[k]
        dd2[k].append(dd[k])

    wanted_keys = ['task_type', 'task_name', 'url', 'description', 'tag',
                   'external_id']
    final_dict = OrderedDict([(a, dd2[a]) for a in wanted_keys if a in dd2])
    f1.write('\t'.join(final_dict.keys()) + '\n')
    for b in zip(*final_dict.values()):
      f1.write('\t'.join(b) + '\n')


def soccer_dedup(str1, str2):
  """converts raw data to thali format for mlb leagues."""
  print 'soccer dedup script invoked'
  f = open(str1, 'r')
  data = f.read().strip()
  data = data.split('\n')
  header = data[0]
  header = header.split('\t')
  # print header
  dd = defaultdict(list)
  list1 = []

  for i in data:
    key = re.findall(r'\d{8}.*', i)
    key = tuple(key)
    value = re.findall(r'^(.*?)\t\d{8}#', i)
    new = OrderedDict(zip(key, value))
    list1.append(new)

    for x in range(0, len(key)):
      dd[key[x]] = []
      dd = OrderedDict(dd)

  tag = tuple(dd.keys())
  dd2 = defaultdict(list)

  with open(str2, 'w') as f1:
    f1.write(header[0] + '\t' + header[1] + '\t' + header[2] +
             '\t' + header[3] +
             '\t' + header[4] + '\t' + header[-1] + '\n')
    for row in list1:
      for k in tag:
        if k not in row.keys():
          continue
        else:
          dd[k] = row[k]
        dd2[k].append(dd[k])

    for v1, v2 in dd2.items():
      f1.write(v2[0] + '\t' + v1 + '\n')
