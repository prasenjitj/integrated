"""This script converts nfl raw data to thali format.

It takes two arguments raw input data file and thali converted output file.
usage : $ python sportsRoster.py nfl_raw.tsv nfl_thali.py.
"""
from collections import defaultdict
from collections import OrderedDict
import re
KEY_MAP = {'Practice Squad': 'SPLGROUSNfl',
           'Reserve/Injured': 'SPLGROUSNflMar14',
           'Reserve/Future': 'SPLGROSTNfl',
           'Reserve/Non-Football Injury': 'SPLGROUSNflMar14',
           'Free Agent Signing': 'SPLGROSTNfl',
           'Suspension Lifted by Commissioner': 'SPLGROUSNflMar14',
           'Practice Squad; Injured': 'SPLGROUSNfl',
           'Waived, No Recall': 'SPLGROSTNfl',
           'Terminated (by Club) from Practice Squad': 'SPLGROUSNfl',
           'Terminated, Vested Veteran, all contracts': 'SPLGROSTNfl',
           'Waived, Failed Physical': 'SPLGROSTNfl',
           'Reserve/Retired': 'SPLGROSTNfl',
           'Terminated, Vested Veteran, Failed Physical': 'SPLGROSTNfl',
           'Waived, Non-Football Injury': 'SPLGROSTNfl',
           'Waived, Non-Football Illness': 'SPLGROSTNfl',
           'Unrestricted Free Agent Signing': 'SPLGROSTNfl',
           'Terminated, Vested Veteran, Post-June 1 Designation':
           'SPLGROUSNflMar14',
           'Traded': 'SPLGROSTNfl',
           'Exclusive Rights Signing': 'SPLGROUSNflMar14',
           'Terminated (by Player) from Practice Squad': 'SPLGROUSNfl',
           'Acquired via First Refusal': 'SPLGROSTNfl'}


def nfl_thali(infile, outfile):
  """converts raw data to thali format for nfl leagues."""
  print 'nfl_thali script invoked'

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
    new_url = value[0]
    new_url = re.sub(r'\s*REC#\s* ', '#', new_url)
    # print type(new_url)
    # print new_url
    value[0] = new_url
    # print value[0]
    new_dic = OrderedDict(zip(key, value))
    # print new
    list1.append(new_dic)

  record = list1
  # print record

  for row_j in record:
    task_name = row_j['Player Name']
    row_j['task_name'] = task_name
    date = row_j['Date']
    date = re.sub(r'-', '', date)
    row_j['date'] = date
    ex_id = row_j['date'] + '#' + row_j['Player Name'] + '#' + row_j['Team']
    ex_id2 = row_j[
        'date'] + '#' + row_j['Player Name'] + '#' + row_j['Team'] + '#' + row_j[
            'Transaction_description']
    # print  ex_id
    description = ('*Find or create each transaction and curate as'
                   ' per guidelines* Player Name: ') + row_j['Player Name'] + (
                       ' # Team: ') + row_j['Team'] + ' # Date: ' + row_j[
                           'Date'] + ' # URL: ' + row_j['url']
    task_type = '/american_football/football_player'
    row_j['description'] = description
    row_j['external_id_old'] = ex_id
    row_j['external_id'] = ex_id2
    row_j['task_type'] = task_type
    url = row_j['url']
    url = re.sub(r' REC#.*', '', url)
    row_j['url'] = url
    tag = row_j['Transaction_description']
    row_j['tag'] = tag

    if row_j['tag'] not in KEY_MAP.keys():
      new_tags.add(row_j['tag'])

    for row_k, row_v in KEY_MAP.items():
      if row_j['tag'] == row_k:
        tag = row_v
        row_j['tag'] = tag
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
