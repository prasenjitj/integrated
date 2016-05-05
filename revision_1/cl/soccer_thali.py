"""This script converts soccer raw data to thali format and dedupes it.

It takes two arguments raw input data file and thali converted output file.
usage : $ python sportsRoster.py soccer_raw.tsv soccer_thali.py.
"""
from collections import defaultdict
from collections import OrderedDict
import re
KEY_MAP = {
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
    'UNG1': 'SPLGROSTHun'}


def soccer_thali(infile, outfile):
  """converts raw data to thali format for mlb leagues."""
  print 'soccer thali script invoked'

  fread = open(infile, 'r')

  data = fread.read().strip()
  data = data.split('\n')
  header = data[0]
  dic1 = defaultdict(list)
  list1 = []
  list2 = []

  key = header.split('\t')

  for row_i in range(1, len(data)):
    value = data[row_i]
    value = value.split('\t')
    # print value
    if value[9] != '2016':
      value = ''
    new_dic = OrderedDict(zip(key, value))
    # print new
    if new_dic:

      list1.append(new_dic)
    else:
      pass
      # print 'dictionary is empty'
  record = list1
  # print record
  for row_j in record:
    url = row_j['url']

    url = re.sub(r'\s*REC#\s*', '/', url)
    url = re.sub(r'\\', '/', url)
    url = re.sub(r'\d{4}-\d{2}-\d{2}', '', url)
    row_j['url'] = url
    for k, v in KEY_MAP.items():
      if row_j['code'] == k:
        tag = v
        row_j['tag'] = tag
    description = ('*Find or create each transaction and curate'
                   'as per guidelines* Player Name: ')
    description += row_j['Player_name']
    description += ' # From Team: ' + row_j['From_Team']
    description += ' # To Team: ' + row_j['To_Team']
    description += ' # Transaction Date: ' + row_j['Date']
    description += ' # URL: ' + row_j['url']
    task_type = '/soccer/football_player'
    row_j['description'] = description
    row_j['Task_Type'] = task_type
    list2.append(row_j)

  for row_x in list2:
    tag = row_x.keys()
    tag = tuple(tag)

  dic2 = defaultdict(list)

  with open(outfile, 'w') as fwrite:
    for row in list2:
      for k in tag:
        if k not in row.keys():
          dic1[k] = ''
        else:
          dic1[k] = row[k]
        dic2[k].append(dic1[k])

    wanted_keys = ['task_type', 'task_name', 'url', 'description', 'tag',
                   'external_id']
    final_dict = OrderedDict([(a, dic2[a]) for a in wanted_keys if a in dic2])
    fwrite.write('\t'.join(final_dict.keys()) + '\n')
    for b in zip(*final_dict.values()):
      fwrite.write('\t'.join(b) + '\n')


def soccer_dedup(infile, outfile):
  """converts raw data to thali format for mlb leagues."""
  print 'soccer dedup script invoked'
  fread = open(infile, 'r')
  data = fread.read().strip()
  data = data.split('\n')
  header = data[0]
  header = header.split('\t')
  dic1 = defaultdict(list)
  list1 = []

  for row_i in data:
    key = re.findall(r'\d{8}.*', row_i)
    key = tuple(key)
    value = re.findall(r'^(.*?)\t\d{8}#', row_i)
    new_dic = OrderedDict(zip(key, value))
    list1.append(new_dic)

    for x in range(0, len(key)):
      dic1[key[x]] = []
      dic1 = OrderedDict(dic1)

  tag = tuple(dic1.keys())
  dic2 = defaultdict(list)

  with open(outfile, 'w') as fwrite:
    fwrite.write(
        header[0] + '\t' + header[1] + '\t' + header[2] +
        '\t' + header[3] + '\t' + header
        [4] + '\t' + header[-1] + '\n')
    for row in list1:
      for k in tag:
        if k not in row.keys():
          continue
        else:
          dic1[k] = row[k]
        dic2[k].append(dic1[k])

    for row_v1, row_v2 in dic2.items():
      fwrite.write(row_v2[0] + '\t' + row_v1 + '\n')
