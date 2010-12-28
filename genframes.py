#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# genframes.py - PPM to "LoL shield" C array converter
#
# Copyright (c) 2010 András Veres-Szentkirályi
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import sys

try:
	width = int(sys.argv[1])
	height = int(sys.argv[2])
	pixels = int(sys.argv[3])
	numframes = int(sys.argv[4])
except:
	print 'Usage: genframes.py <width> <height> <number of frames>'
	sys.exit(1)

# Table for LED Position in leds[] ram table (from Charlieplexing.cpp)
ledMap = [
    13, 5,13, 6,13, 7,13, 8,13, 9,13,10,13,11,13,12,13, 4, 4,13,13, 3, 3,13,13, 2, 2,13,
    12, 5,12, 6,12, 7,12, 8,12, 9,12,10,12,11,12,13,12, 4, 4,12,12, 3, 3,12,12, 2, 2,12,
    11, 5,11, 6,11, 7,11, 8,11, 9,11,10,11,12,11,13,11, 4, 4,11,11, 3, 3,11,11, 2, 2,11,
    10, 5,10, 6,10, 7,10, 8,10, 9,10,11,10,12,10,13,10, 4, 4,10,10, 3, 3,10,10, 2, 2,10,
     9, 5, 9, 6, 9, 7, 9, 8, 9,10, 9,11, 9,12, 9,13, 9, 4, 4, 9, 9, 3, 3, 9, 9, 2, 2, 9,
     8, 5, 8, 6, 8, 7, 8, 9, 8,10, 8,11, 8,12, 8,13, 8, 4, 4, 8, 8, 3, 3, 8, 8, 2, 2, 8,
     7, 5, 7, 6, 7, 8, 7, 9, 7,10, 7,11, 7,12, 7,13, 7, 4, 4, 7, 7, 3, 3, 7, 7, 2, 2, 7,
     6, 5, 6, 7, 6, 8, 6, 9, 6,10, 6,11, 6,12, 6,13, 6, 4, 4, 6, 6, 3, 3, 6, 6, 2, 2, 6,
     5, 6, 5, 7, 5, 8, 5, 9, 5,10, 5,11, 5,12, 5,13, 5, 4, 4, 5, 5, 3, 3, 5, 5, 2, 2, 5,
    ]

def _BV(bit):
	return 1 << bit

def img2buf(img, maxval):
	buf = [0 for i in range(pixels)]
	treshold = maxval / 2
	pixel = 0
	for y in range(height):
		for x in range(width): # based on Charlieplexing.cpp
			pin_low  = ledMap[x * 2 + y * 28 + 1]
			pin_high = ledMap[x * 2 + y * 28 + 0]
			r = ord(img[pixel])
			pixel += 1
			g = ord(img[pixel])
			pixel += 1
			b = ord(img[pixel])
			pixel += 1
			if (r + g + b) / 3 > treshold:
				buf[(pin_low - 2) * 2 + (pin_high / 8)] |= _BV(pin_high & 0x07)
			else:
				buf[(pin_low - 2) * 2 + (pin_high / 8)] &= ~_BV(pin_high & 0x07)
	return ', '.join(map(str, buf))

for i in range(numframes):
	fn = '%08d.ppm' % (i + 1)
	f = open(fn, 'r')
	if f.readline() != 'P6\n':
		print 'invalid image: must be binary PPM'
		continue
	if f.readline() != '%d %d\n' % (width, height):
		print 'invalid image: resolution must be 14 x 9'
		continue
	maxval = int(f.readline())
	img = f.read()
	if len(img) != width * height * 3:
		print 'invalid file length: %d byte(s)' % len(img)
		continue
	if i != 0:
		print ','
	print '{ %s }' % img2buf(img, maxval)
	sys.stderr.write('.')
