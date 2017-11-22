#! /usr/bin/python
"""
Prepare a given case and run it

Input:
  - Path to ZipFile of cases
  - 'Name' of the given case from preprocess.py
  - Path to place the resulting tar

Runs in the context of the 'paralllelworks/radiance' Docker container

"""
import os
import subprocess
import sys
import zipfile
import csv

# Relevant paths in Energyplus Docker container
ENERGYPLUS_DIR = "/opt/EnergyPlus-8-5-0"

# Open the cases zipfile
try:
  CASES_PATH = sys.argv[1]
  CASE_NAME = sys.argv[2]
  OUT_PATH = sys.argv[3]
  CSV_PATH = sys.argv[4]
  RUN_DIR = CASE_NAME
  EP_OUTPUT = RUN_DIR + "/Output"
  cases = zipfile.ZipFile(CASES_PATH, 'r')
  names = cases.namelist()
except (IndexError, IOError) as e:
  print 'Cases zip file could not be found and/or case not given'
  raise e
  
# Find the epw and idf files
ep_names = [name for name in names if 'honeybee_energyplus' in name]
epw_file_paths = [name for name in ep_names if CASE_NAME + "/" in name and ".epw" in name]
idf_file_paths = [name for name in ep_names if CASE_NAME + "/" in name and ".idf" in name]
print epw_file_paths
print idf_file_paths

# Get path to case's epw file
case_epw_file_path = [name for name in epw_file_paths if CASE_NAME in name]
if len(case_epw_file_path) != 1:
  raise Exception('Found more than one .epw file for "{}" case'.format(CASE_NAME))
case_epw_file_path = case_epw_file_path[0]


# Get path to case's idf file
case_idf_file_path = [name for name in idf_file_paths if CASE_NAME in name]
if len(case_idf_file_path) != 1:
  raise Exception('Found more than one .idf file for "{}" case'.format(CASE_NAME))
case_idf_file_path = case_idf_file_path[0]

# Find filename of epw and idf, without path
case_epw = str(os.path.basename(case_epw_file_path))
case_idf = str(os.path.basename(case_idf_file_path))


# Set enviroment variables
my_env = os.environ
my_env["ENERGYPLUS_DIR"] = ENERGYPLUS_DIR
my_env["PATH"] = ENERGYPLUS_DIR + ":" + my_env["PATH"]


# Extract remaining case files and run the case
case_files = [f for f in names if CASE_NAME in f]
cases.extractall(members=case_files)



# Format cases for runenergyplus
case_epw = case_epw.replace(".epw", "")
case_idf = case_idf.replace(".idf","")

# Call Energy Plus
subprocess.call(["runenergyplus",case_idf, case_epw],cwd=RUN_DIR, env=my_env)

# Get path to CSV File
ep_output_names = os.listdir(EP_OUTPUT)
csv_names = [name for name in ep_output_names if 'Zsz.csv' not in name and '.csv' in name]
print csv_names
if len(csv_names) != 1:
  raise Exception('Found more than one .csv file for "{}" case'.format(CASE_NAME))
csv_path = EP_OUTPUT + "/" + csv_names[0]
total_path = RUN_DIR + os.path.basename(CSV_PATH)

# Read CSV File and sum total columns
with open(csv_path, 'rb') as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  total1 = 0
  total2 = 0
  total3 = 0
  total4 = 0
  for row in reader:
    header_row = ["TOTALS", row[1], row[2], row[3], row[4]]
    break
  for row in reader:
    total1 += float(row[1])
    total2 += float(row[2])
    total3 += float(row[3])
    total4 += float(row[4])
  totals = ["Total", total1, total2, total3, total4]
  
# Write CSV File with totals
with open(total_path, 'w+b') as csvwrite:
  writer = csv.writer(csvwrite, delimiter=',')
  writer.writerow(header_row)
  writer.writerow(totals)
  
  
# Copy total.csv outside of tarball
subprocess.call(['cp', total_path, CSV_PATH])

# Tar run directory and all outputs files
subprocess.call(['tar', '-czf', OUT_PATH, "-C", RUN_DIR, "."])

