#!/usr/bin/env python
# encoding: utf-8
"""
skype2prowl.py

Created by Kohichi Aoki on 2009-08-05.
Copyright (c) 2009 drikin.com. All rights reserved.
"""

import sys
import os
import getopt
import Skype4Py
import prowlpy

PROWL_API_KEY	    = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
OWN_DISPLAY_NAME  = ""

skype 			= Skype4Py.Skype()
prowl 			= prowlpy.Prowl(PROWL_API_KEY)

help_message = '''
The help message goes here.
'''

# ----------------------------------------------------------------------------------------------------
# Fired on attachment status change. Here used to re-attach this script to Skype in case attachment is lost. Just in case.
def OnAttach(status):
  print 'API attachment status: ' + skype.Convert.AttachmentStatusToText(status)

  if status == Skype4Py.apiAttachAvailable:
    skype.Attach();

  if status == Skype4Py.apiAttachSuccess:
    print('******************************************************************************');

def OnMessageStatus(Message, Status):
	if Status == 'RECEIVED' or Status == 'SENT':
		topic = Message.Chat.Topic[:10]
		displayName = Message.FromDisplayName
		if Status == 'RECEIVED' and displayName != OWN_DISPLAY_NAME:
			message = displayName + ': ' + Message.Body
			sendNotification('Skype', topic, message)
		if Status == 'SENT':
			message = 'Myself: ' + Message.Body

def sendNotification(appname, event, description):
	if( not PROWL_API_KEY ):
		return
	try:
		print appname + ' ' + event + ': ' + description
		prowl.add(appname.encode('utf-8'), event.encode('utf-8'), description.encode('utf-8'))
	except Exception,msg:
	  print msg

class Usage(Exception):
  def __init__(self, msg):
    self.msg = msg

def main(argv=None):
  if argv is None:
    argv = sys.argv
  try:
    try:
      opts, args = getopt.getopt(argv[1:], "hu:k:v", ["help", "user", "api_key"])
    except getopt.error, msg:
      raise Usage(msg)
  
    # option processing
    for option, value in opts:
      if option == "-v":
        verbose = True
      if option in ("-h", "--help"):
        raise Usage(help_message)
      if option in ("-u", "--user"):
        global OWN_DISPLAY_NAME
        OWN_DISPLAY_NAME = value
      if option in ("-k", "--api_key"):
        global PROWL_API_KEY
        PROWL_API_KEY = value
      
  except Usage, err:
    print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
    print >> sys.stderr, "\t for help use --help"
    return 2
  
  skype.OnAttachmentStatus = OnAttach;
  skype.OnMessageStatus = OnMessageStatus;
  print('******************************************************************************');
  print 'Username      : ' + OWN_DISPLAY_NAME
  print 'Prowl API Key : ' + PROWL_API_KEY
  print 'Connecting to Skype..'
  skype.Attach();
  
  # ----------------------------------------------------------------------------------------------------
  # Looping until user types 'exit'
  Cmd = '';
  while not Cmd == 'exit':
    pass
    Cmd = raw_input('');

if __name__ == '__main__':
  main()

