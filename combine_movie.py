#!/usr/bin/env python
# encoding: utf-8
"""
combine_movie.py

Created by Kohichi Aoki on 2009-08-21.
Copyright (c) 2009 drikin.com. All rights reserved.
"""

import sys, os, popen2
import dircache
import glob
import getopt

MENCODER    = "mencoder %s -o %s -oac pcm -ovc copy"
MP4BOX      = "MP4Box %s -new %s"
OUTPUT_FILE = "combined.mp4"

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
  file_list = ''
  # files = glob.glob(target_path + '/*.MP4')
  for file in files:
    file_path = os.path.join(target_path, file)
    if os.path.isfile(file_path):
      if not file.find('.') == 0:
        file_list += ' "' + file_path + '"'
  command = MENCODER % (file_list, OUTPUT_FILE)
  print command
  p = popen2.Popen3( command )
  for line in p.fromchild:
      print line

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
