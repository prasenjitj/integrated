"""This script converts soccer raw data to thali format and dedupes it.

It takes two arguments raw input data file and thali converted output file.
usage : $ python sportsRoster.py soccer_raw.tsv soccer_thali.py.
"""
from collections import defaultdict
from collections import OrderedDict
import re
import csv
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

"""converts raw data to thali format for mlb leagues."""
row ={}
print 'soccer thali script invoked'
with open('soccer_raw.csv','rb') as csvinput:
  with open ('soccer_thali.csv','wb') as csvoutput:
    reader = csv.DictReader(csvinput)
    fieldnames = ['task_type','task_name','url','external_id','tag','year','description'] 
    writer = csv.DictWriter(csvoutput, fieldnames=fieldnames)
    writer.writeheader()
    
    for row in reader:
      #delete all recodrds before 2016
      if row['Year'] != '2016':
        row = {}
      if row:
        #change url
        url = row['url']
        url = re.sub(r'\s*REC#\s*', '/', url)
        url = re.sub(r'\\', '/', url)
        url = re.sub(r'\d{4}-\d{2}-\d{2}', '', url)
        row['url'] = url
        #map tags
        for k, v in KEY_MAP.items():
          if row['code'] == k:
            tag = v
            row['tag'] = tag
        #construct description
        description = ('*Find or create each transaction and curate'
                   'as per guidelines* Player Name: ')
        description += row['Player_name']
        description += ' # From Team: ' + row['From_Team']
        description += ' # To Team: ' + row['To_Team']
        description += ' # Transaction Date: ' + row['Date']
        description += ' # URL: ' + row['url']
        row['description'] = description
            

      print row
      if row:
        writer.writerow({'task_type':row['task_type'],'task_name':row['task_name'],'url':row['url'],'tag':row['tag'],'year':row['Year'],'description':row['description'],'external_id':row['external_id']}) 
