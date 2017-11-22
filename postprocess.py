#! /usr/bin/python

import os
import subprocess
import sys
import zipfile
import csv

try:
  OUTFILE = sys.argv[1]
  CSVFILE = sys.argv[2]
except (IOError) as e:
  print "Output file didn't work"
  raise e	
    
# Open CSV output file
csvf = open(CSVFILE, 'ab')
writer = csv.writer(csvf, delimiter=',')

# Writes header row
for (dirpath, dirnames, filenames) in os.walk("results"):
    for filename in filenames:
        if filename.endswith('.csv'):
            full_path = os.path.join(dirpath,filename)
            with open(full_path, 'rb') as csvheader:
                reader = csv.reader(csvheader, delimiter=',')
                for row in reader:
                    header_row = ["CASE NAME", row[1], row[2], row[3], row[4]]
                    break
            break

writer.writerow(header_row)

            
# Write to CSV and find files to ZIP
for (dirpath, dirnames, filenames) in os.walk("results"):
    for filename in filenames:
        if filename.endswith('.csv'):
            full_path = os.path.join(dirpath,filename)
            print str(full_path)
            with open(full_path, 'rb') as csvdata:
                reader = csv.reader(csvdata, delimiter=',')
                total_case = full_path.replace(".csv", "")
                reader.next()
                for row in reader:
                    print row
                    writer.writerow([total_case, row[1], row[2], row[3], row[4]])


        if filename.endswith('.tgz'):
            casename=filename.replace(".tgz","")
            subprocess.call(["mkdir",casename],cwd=dirpath)
            subprocess.call(["tar","-xzf",filename,"-C",casename],cwd=dirpath)
            subprocess.call(["rm",filename],cwd=dirpath)
                
# Zip files        
subprocess.call(["zip","-r","results","."],cwd="results")
subprocess.call(["cp","results/results.zip",OUTFILE])

csvf.close()