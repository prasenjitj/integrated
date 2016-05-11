import csv
"""converts raw data to thali format for mlb leagues."""
print 'soccer dedup script invoked'

with open('soccer_thali.csv','rb') as csvinput:
  with open ('soccer_final.csv','wb') as csvoutput:
    reader = csv.DictReader(csvinput)
    fieldnames = ['task_type','task_name','url','external_id','tag','year','description'] 
    writer = csv.DictWriter(csvoutput, fieldnames=fieldnames)
    writer.writeheader()
    entries = set()
    for row in reader:
      key = (row['external_id'])
      if key not in entries:
        writer.writerow(row)
        entries.add(key) 