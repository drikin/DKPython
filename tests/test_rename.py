#!/usr/bin/env python
# encoding: utf-8
"""
test_rename.py

Created by Kohichi Aoki on 2009-12-26.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""
import sys, os
sys.path.append('../')

import unittest
import rename


class untitled(unittest.TestCase):
  def setUp(self):
    pass

  def test_rename(self):
    test_dir = "rename"
    file_names = ["abc.txt",
                  "bcd.mpg",
                  "(20090101)abc.divx",
                  "(20090102) bcd.mpg",
                  "(20090103)   efg.mp4",
                  "[20090101]abc.divx",
                  "[20090102] bcd.mpg",
                  "[20090103]   efg.mp4",
                  "[drama] abc (2009.03.22 1440x1080i x264).mp4",
                  "(drama) abc (2009.03.22 1440x1080i x264).mp4",
                  "Nodame Cantabile in Europe SP2 (2009 Version) [720p x.264 AAC][Ueno Juri].mkv",
                  "2009.Shanghai.Super.Concert.091224.SDTV.XViD-DokGoDie.avi",
                  "2009...Shanghai.Super.Concert.091224.SDTV.XViD-DokGoDie.avi",
                  "2009.10.Shanghai.Super.Concert.091224.SDTV.XViD-DokGoDie.avi",
                  "Abc Def (2009.01.01).mp4"
                  ]
    
    os.mkdir(test_dir)
    for file_name in file_names:
      f = open(os.path.join(test_dir, file_name), "w")
      f.close()
    
    for (root, dirs, files) in os.walk(test_dir):
      for file in files:
        rename.rename(root, file, False)
      
    for file_name in file_names:
      os.remove(os.path.join(test_dir, file_name))
    os.rmdir(test_dir)
    
if __name__ == '__main__':
  unittest.main()