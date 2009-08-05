#!/usr/bin/env python
# encoding: utf-8
"""
skype2prowl.py

Created by Kohichi Aoki on 2009-08-05.
Copyright (c) 2009 drikin.com. All rights reserved.
"""

import sys
import os
import Skype4Py
import prowlpy

PROWL_API_KEY	= "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

skype 			= Skype4Py.Skype()
prowl 			= prowlpy.Prowl(PROWL_API_KEY)

# ----------------------------------------------------------------------------------------------------
# Fired on attachment status change. Here used to re-attach this script to Skype in case attachment is lost. Just in case.
def OnAttach(status):
  print 'API attachment status: ' + skype.Convert.AttachmentStatusToText(status)

  if status == Skype4Py.apiAttachAvailable:
    skype.Attach();

  if status == Skype4Py.apiAttachSuccess:
    print('******************************************************************************');

def OnMessageStatus(Message, Status):
	if (Status == 'RECEIVED' or Status == 'SENT'):
		topic = Message.Chat.Topic[:10]
		if Status == 'RECEIVED':
			message = Message.FromDisplayName + ': ' + Message.Body
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

def main():
  skype.OnAttachmentStatus = OnAttach;
  skype.OnMessageStatus = OnMessageStatus;
  print('******************************************************************************');
  print 'Connecting to Skype..'
  skype.Attach();
  
  # ----------------------------------------------------------------------------------------------------
  # Looping until user types 'exit'
  Cmd = '';
  while not Cmd == 'exit':
    pass
    #Cmd = raw_input('');

if __name__ == '__main__':
  main()

