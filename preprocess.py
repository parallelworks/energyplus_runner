#! /usr/bin/python
"""
Input: path to a Zipfile of Honeybee cases
Generate list of paths to cases based on presence of a .bat file
"""

import os
import sys
import zipfile

ZIP_PATH = sys.argv[1]

try:
  cases = zipfile.ZipFile(ZIP_PATH, 'r')
  names = cases.namelist()
except IOError as e:
  print 'Cases zip file could not be found'
  raise e

# Temporary filter out of non-radiance cases
rad_names = [name for name in names if 'honeybee_energyplus' in name]
bat_file_paths = [name for name in rad_names if '.bat' in name]
cases_root_paths = [os.path.dirname(p) for p in bat_file_paths if len(p) > 0]

for p in cases_root_paths:
  print p