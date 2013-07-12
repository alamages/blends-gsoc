#!/usr/bin/env python

# Copyright 2013: Emmanouil Kiagias <e.kiagias@gmail.com>
# License: GPL

"""
this module is still under construction, just testing stuff around
before I write the complete script
"""

import re
import pprint
import logging
from debian import deb822

#code taken from udd/blends_metadata_gathener.py
def clean_up_packages(packages):
  logger = logging.getLogger(__name__)
  # Hack: Debian Edu tasks files are using '\' at EOL which is broken
  #       in RFC 822 files, but blend-gen-control from blends-dev relies
  #       on this.  So remove this stuff here for the Moment
  pkgs = re.sub('\\\\\n\s+', '', packages)

  # Remove versions from versioned depends
  pkgs = re.sub(' *\([ ><=\.0-9]+\) *', '', pkgs)

  # temporary strip spaces from alternatives ('|') to enable erroneous space handling as it was done before
  pkgs = re.sub('\s*\|\s*', '|', pkgs)

  # turn alternatives ('|') into real depends for this purpose
  # because we are finally interested in all alternatives
  pkgslist = pkgs.split(',')
  # Collect all dependencies in one line first,
  # create an object for each later
  pkgs_in_one_line = []
  for depl in pkgslist:
    dl = depl.strip()
    if dl != '': # avoid confusion when ',' is at end of line
      if re.search('\s', dl):
        logger.error("Blend %s task %s: Syntax error '%s'" % (blend, task, dl))
        # trying to fix the syntax error after issuing error message
        dlspaces = re.sub('\s+', ',', dl).split(',')
        for dls in dlspaces:
          pkgs_in_one_line.append(dls.strip())
          logger.info("Blend %s task %s: Found '%s' package inside broken syntax string - please fix task file anyway" % (blend, task, dls.strip()))
      else:
        # in case we have to deal with a set of alternatives
        if re.search('\|', dl):
          #for da in dl.split('|'):
          #  deps_in_one_line.append(da)
          dl = re.sub('\|', ' | ', dl)
        pkgs_in_one_line.append(dl)
        # self.inject_package_alternatives(blend, task, strength, dl)

  return pkgs_in_one_line

def load_task(path_to_task):
  """
  parses a task file and return a dictionary containing all its package headers elements
  (depends, suggests etc)
  """
	ftask = open(path_to_task, 'r')

	taskinfo = {}
	for header in ["depends", "suggests", "recommends", "avoid", "ignore"]:
		taskinfo[header] = []

	for paragraph in deb822.Sources.iter_paragraphs(ftask, shared_storage=False):
		if paragraph.has_key("task"):
			taskinfo["task"] = paragraph["task"]

		if paragraph.has_key("depends"):
			taskinfo["depends"] += clean_up_packages(paragraph["depends"])

		if paragraph.has_key("suggests"):
			taskinfo["suggests"] += clean_up_packages(paragraph["suggests"])

		if paragraph.has_key("recommends"):
			taskinfo["recommends"] += clean_up_packages(paragraph["recommends"])

		if paragraph.has_key("ignore"):
			taskinfo["ignore"] += clean_up_packages(paragraph["ignore"])

		if paragraph.has_key("avoid"):
			taskinfo["avoid"] += clean_up_packages(paragraph["avoid"])

	return taskinfo

#in this function the input lists must be sorted
def diff_sets(a_list, b_list):
  """
  return the elements which appear in a_list and not in b_list
  for example it can be used to compare two tasks from different releases
  and check which packages where removed/added.
  Note: in this function the input lists must be sorted
  """
  diffs = []
  b_index = 0
  b_list_len = len(b_list)

  for a_index, a in enumerate(a_list):
    for b in b_list[b_index:]:
      if a == b:
        b_index += 1
        break
      if a > b:
        b_index += 1

        if b_index + 1 == b_list_len:
          diffs += a_list[a_index:]
          break

        continue
      if a < b:
        diffs.append(a)
        break

    if b_index + 1 >= b_list_len:
      break

  return diffs


#the input lists do not need to be sorted
def diff_quicksort(a_list, b_list):
  """
  return the elements which appear in a_list and not in b_list
  for example it can be used to compare two tasks from different releases
  and check which packages where removed/added, a quicksort-similar algorithm is used
  """
  #value + reference
  a_array = [ { 'value' : a, 'ref' : False } for a in a_list ]
  b_array = [ { 'value' : b, 'ref' : True } for b in b_list ]
 
  return [ d['value'] for d in  do_diff_quicksort(a_array+b_array) ]

#same results as diff_sets
#element_array: a+b and reference_array: b
def do_diff_quicksort(element_array):
  array_len = len(element_array)
  if  array_len <= 1:
    if element_array:
      if element_array[0]['ref']:
        return []
    return element_array

  #here we choose a pivot the middle element of the list
  pivot_index = int(array_len / 2)
  pivot = element_array[pivot_index]
  
  #remove pivot from list:
  del element_array[pivot_index]

  less = []
  greater = []

  include_pivot = True
  for x in element_array:
    if x['value'] < pivot['value']:
      less.append(x)
    elif x['value'] > pivot['value']:
      greater.append(x)
    else:
      include_pivot = False

  if include_pivot and not pivot['ref']:
    return do_diff_quicksort(less) + [pivot] + do_diff_quicksort(greater)
  else:
    return do_diff_quicksort(less) + do_diff_quicksort(greater)


tasks_path = "trunk/debian-med/tasks"
#yaw = load_task('/home/alamagestest/Projects/blends/projects/med/trunk/debian-med/tasks/bio')

#these are already sorted
spackages =  ['im-switch', 'java-gcj-compat',                     'kasteroids', 'katomic', 'kbabel', 'kbackgammon', 'kbattleship', 'lightspeed', 'mdns-scan', 'monopd', 'mozilla-mplayer']
spackages2 = [             'java-gcj-compat', 'kaffeine-mozilla',               'katomic', 'kbabel', 'kbackgammon', 'kbattleship',               'mdns-scan', 'monopd', 'mozilla-mplayer', 'mozilla-openoffice.org']
 
#print diff_sets(packages, packages2)
#print diff_sets(sorted(['x', 'y', 'z']), packages2)
#pprint.pprint(yaw, indent=4)
packages = [  'monopd', 'mozilla-mplayer', 'im-switch','java-gcj-compat', 'kaffeine-mozilla', 'kasteroids', 'katomic', 'kbabel', 'kbackgammon', 'kbattleship', 'lightspeed', 'mozilla-openoffice.org']
packages2 = [ 'mdns-scan', 'monopd', 'mozilla-mplayer',             'java-gcj-compat', 'kaffeine-mozilla',               'katomic', 'kbabel', 'kbackgammon', 'kbattleship',               'mozilla-openoffice.org']
packages3 = ['x', 'y', 'z']
print diff_quicksort( packages, packages2)

print diff_sets(spackages, spackages2)