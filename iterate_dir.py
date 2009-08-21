#!/usr/bin/env python
# encoding: utf-8
"""
iterate_dir.py

Created by Kohichi Aoki on 2009-08-21.
Copyright (c) 2009 drikin.com. All rights reserved.
"""

import sys, os
import dircache
import getopt


help_message = '''
The help message goes here.
'''


class Usage(Exception):
  def __init__(self, msg):
    self.msg = msg

def iterate_dir(target_path):
  if not os.path.exists(target_path) or not os.path.isdir(target_path):
    print "Error: Target path is not exist. Path:" + target_path
    exit
  
  files = dircache.listdir(target_path)
  for file in files:
    if os.path.isfile(os.path.join(target_path, file)):
      print file

def main(argv=None):
  if argv is None:
    argv = sys.argv
    if len(argv) > 1:
      target = argv[1]
    else:
      target = os.path.expanduser(u'~')

  try:
    try:
      opts, args = getopt.getopt(argv[1:], "ho:v", ["help", "output="])
    except getopt.error, msg:
      raise Usage(msg)
    
    # option processing
    for option, value in opts:
      if option == "-v":
        verbose = True
      if option in ("-h", "--help"):
        raise Usage(help_message)
      if option in ("-o", "--output"):
        output = value
  
  except Usage, err:
    print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
    print >> sys.stderr, "\t for help use --help"
    return 2

  iterate_dir(target)

if __name__ == "__main__":
  sys.exit(main())
