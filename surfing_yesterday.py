#!/usr/bin/env python
# encoding: utf-8
"""
surfing_yesterday.py

Created by Kohichi Aoki on 2009-07-22.
Copyright (c) 2009 drikin.com. All rights reserved.
"""

import os
import Image, ImageDraw, ImageFont
import datetime

OUTPUT_DIR				= os.path.expanduser("~/Desktop/")
SOURCE_DIR 				= "~/Library/Caches/com.apple.Safari/"
MD_QUERY				= "(kMDItemContentType == \"jpeg\"wc && kMDItemFSContentChangeDate > $time.yesterday && kMDItemFSContentChangeDate < $time.today)"
#MD_QUERY				= "(kMDItemContentType == \"jpeg\"wc && kMDItemFSContentChangeDate > $time.today)"

THUMBNAIL_WIDTH_MAX		= 128
THUMBNAIL_HEIGHT_MAX	= 256

HORIZONAL_COUNT_MAX		= 20

def mdfind(dir, query):
	cmd = """ mdfind -onlyin %s '%s' """ % (dir, query)
	stdout_handle = os.popen(cmd, "r")
	text = stdout_handle.read()
	return text.split("\n")
	
def getOutputSize(count, horizonalCountMax):
	if count < horizonalCountMax:
		return (THUMBNAIL_WIDTH_MAX * count, THUMBNAIL_HEIGHT_MAX)
	elif (count % horizonalCountMax) > 0:
		return (THUMBNAIL_WIDTH_MAX * horizonalCountMax, THUMBNAIL_HEIGHT_MAX * ((count / horizonalCountMax) + 1))
	else:
		return (THUMBNAIL_WIDTH_MAX * horizonalCountMax, THUMBNAIL_HEIGHT_MAX * (count / horizonalCountMax))

def main():
	files = mdfind(SOURCE_DIR, MD_QUERY)
	image_count = len(files) - 1
	print '''count: %d''' % image_count
	size = getOutputSize(image_count, HORIZONAL_COUNT_MAX)
	print "output size: %d, %d" % (size[0], size[1])	
	background_color = (0,0,0) # black
	output_image = Image.new('RGB', size, background_color)

	for i in range((image_count / HORIZONAL_COUNT_MAX) + 1):
		for j in range(HORIZONAL_COUNT_MAX):
			try:
				source_image = Image.open(files[(i * HORIZONAL_COUNT_MAX) + j])
				source_image.thumbnail((THUMBNAIL_WIDTH_MAX, THUMBNAIL_HEIGHT_MAX))
				size = source_image.getbbox()
				region = source_image.crop(size)
				output_image.paste(region, (THUMBNAIL_WIDTH_MAX * j, THUMBNAIL_HEIGHT_MAX * i, source_image.size[0] * (j + 1), source_image.size[1] + THUMBNAIL_HEIGHT_MAX * i))
				source_image.close()
			except:
				pass
	today = datetime.date.today()
	draw = ImageDraw.Draw(output_image)
	font = ImageFont.truetype("/System/Library/Fonts/AppleGothic.ttf" , 30)
	footer_text = str(image_count) + 'sites ' + (today - datetime.timedelta(1)).isoformat()
	draw_color = "#E42063" # Rose Red
	draw.text((20, output_image.size[1]-40), footer_text, font=font, fill=draw_color)
	
	output_filename = OUTPUT_DIR + 'webthumbail_' + (today - datetime.timedelta(1)).isoformat() + '.jpg'
	output_image.save(output_filename, "JPEG")
	os.popen("open " + output_filename)
	
if __name__ == '__main__':
	main()
