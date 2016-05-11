
"""converts raw data to thali format for mlb leagues."""
print 'soccer dedup script invoked'

with open('soccer_thali.csv','rb') as csvinput:
  with open ('soccer_final.csv','wb') as csvoutput:
    reader = csv.DictReader(csvinput)
    fieldnames = ['task_type','task_name','url','external_id','tag','year','description'] 
    writer = csv.DictWriter(csvoutput, fieldnames=fieldnames)
    writer.writeheader()
    
    for row in reader:
      row['external_id'] =
