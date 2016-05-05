"""This script dedupes soccer thali format data.

It takes two arguments thali format data file and soccer final tsv.
"""
from collections import defaultdict
from collections import OrderedDict
import re


def soccer_dedup(str1, str2):
  """Dedupes soccer thali format data."""
  print 'soccer dedup script invoked'
  f = open(str1, 'r')
  data = f.read().strip()
  data = data.split('\n')
  header = data[0]
  header = header.split('\t')
  print header[-1]
  dd = defaultdict(list)
  # print data
  list1 = []

  for i in data:
    key = re.findall(r'\d{8}.*', i)
    key = tuple(key)
    # print 'key :: ',key
    value = re.findall(r'^(.*?)\t\d{8}', i)
    # value=''.join(value)
    # value=re.sub(r'\s*REC#.*','',value).split()
    # print type(value)
    print 'value :: ', value
    new = OrderedDict(zip(key, value))
    # print new
    list1.append(new)
    # print list1

    for x in range(0, len(key)):
      dd[key[x]] = []
      dd = OrderedDict(dd)
    # print dd
  tag = tuple(dd.keys())
  # print tag

  dd2 = defaultdict(list)

  with open(str2, 'w') as f1:
    f1.write(
        header[-1] + '\t' + header[0] + '\t' + header[1] + '\t' +
        header[2] + '\t' + header[3] + '\n')
    for row in list1:
      # print row
      for k in tag:
        if k not in row.keys():
          # dd[k] = ''
          # print 'false'
          continue
        else:
          # print k
          dd[k] = row[k]
          # print 'true'
        dd2[k].append(dd[k])
    # print dd2

    for v1, v2 in dd2.items():
      # print '-----------'
      # print v1,'#######',v2[0]

      f1.write(v1 + '\t' + v2[0] + '\n')
