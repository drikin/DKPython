#!/usr/bin/env python
# encoding: utf-8
"""
rename.py

Created by Kohichi Aoki on 2009-12-24.
Copyright (c) 2009 drikin.com. All rights reserved.
"""

import os, sys
import getopt
import re

help_message = '''
The help message goes here.
'''
_patterns = [r'^\s*',
             r'\s?[\(|\[](.*?)[\)|\]][\s|\.]*',
             r'\.?\d{2,4}[-|/|_|\.]?\d{1,2}[-|/|_|\.]?\d{1,2}',
             r'^\s*',
             r'^\.+']

class Usage(Exception):
  def __init__(self, msg):
    self.msg = msg

def rename(path, file, execute=False):
  print('orginal: ' + file)
  
  # find date string
  p = re.compile(r'(\d{2,4})[-|/|_|\.]?(\d{1,2})[-|/|_|\.]?(\d{1,2})')
  m = p.search(file)
  root, ext = os.path.splitext(file)
  new = root

  for pattern in _patterns:
    p = re.compile(pattern)
    new = p.sub('', new)
  if m:
    new = new + ' (' + m.group(1) + m.group(2) + m.group(3) + ')' + ext
  print('    new: ' + new)
  if execute:
    os.rename(os.path.join(path, file), os.path.join(path, new))

def main(argv=None):
  if argv is None:
    argv = sys.argv
  try:
    try:
      opts, args = getopt.getopt(argv[1:], "ho:d:vx", ["help", "output=", "dir="])
    except getopt.error, msg:
      raise Usage(msg)
  
    execute = False
    # option processing
    for option, value in opts:
      if option == "-v":
        verbose = True
      if option == "-x":
        execute = True
      if option in ("-h", "--help"):
        raise Usage(help_message)
      if option in ("-d", "--dir"):
        target = value
      if option in ("-o", "--output"):
        output = value
  
    for (root, dirs, files) in os.walk(target):
      for file in files:
        rename(root, file, execute)
          
  except Usage, err:
    print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
    print >> sys.stderr, "\t for help use --help"
    return 2


if __name__ == "__main__":
  sys.exit(main())
