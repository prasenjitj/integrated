"""This script converts nfl raw data to thali format.

It takes two arguments raw input data file and thali converted output file.
usage : $ python sportsRoster.py nfl_raw.tsv nfl_thali.py.
"""
from collections import defaultdict
from collections import OrderedDict
import re


def nfl_thali(str1, str2):
  """converts raw data to thali format for nfl leagues."""
  print 'nfl_thali script invoked'

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
      'Practice Squad': 'SPLGROUSNfl',
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
      'Terminated, Vested Veteran, Post-June 1 Designation': 'SPLGROUSNflMar14',
      'Traded': 'SPLGROSTNfl',
      'Exclusive Rights Signing': 'SPLGROUSNflMar14',
      'Terminated (by Player) from Practice Squad': 'SPLGROUSNfl',
      'Acquired via First Refusal': 'SPLGROSTNfl'
  }

  key = header.split('\t')
  # print key
  #
  for i in range(1, len(data)):
    value = data[i]
    value = value.split('\t')
    new_url = value[0]
    new_url = re.sub(r'\s*REC#\s* ', '#', new_url)
    # print type(new_url)
    # print new_url
    value[0] = new_url
    # print value[0]
    new = OrderedDict(zip(key, value))
    # print new
    list1.append(new)

  record = list1
  # print record

  for j in record:
    task_name = j['Player Name']
    j['task_name'] = task_name
    date = j['Date']
    date = re.sub(r'-', '', date)
    j['date'] = date
    ex_id = j['date'] + '#' + j['Player Name'] + '#' + j['Team']
    ex_id2 = j[
        'date'] + '#' + j['Player Name'] + '#' + j['Team'] + '#' + j[
            'Transaction_description']
    # print  ex_id
    description = ('*Find or create each transaction and curate as'
                   ' per guidelines* Player Name: ') + j['Player Name'] + (
                       ' # Team: ') + j['Team'] + ' # Date: ' + j[
                           'Date'] + ' # URL: ' + j['url']
    task_type = '/american_football/football_player'
    j['description'] = description
    j['external_id_old'] = ex_id
    j['external_id'] = ex_id2
    j['task_type'] = task_type
    url = j['url']
    url = re.sub(r' REC#.*', '', url)
    j['url'] = url
    tag = j['Transaction_description']
    j['tag'] = tag

    if j['tag'] not in mapping.keys():
      new_tags.add(j['tag'])

    for k, v in mapping.items():
      if j['tag'] == k:
        tag = v
        j['tag'] = tag
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
