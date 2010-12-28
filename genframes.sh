#!/bin/bash
#
# genframes.sh - video to "LoL shield" C file converter
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

INPUT=~/_mm/demo/kewlers_mfx-1995.avi
OUTPUT=frames.h
START=176 # input start in seconds
FRAMES=500 # input frames
WIDTH=14
HEIGHT=9
PIXELS=24

FPS=$(mplayer $INPUT -vf scale=$WIDTH:$HEIGHT -ss $START -frames $FRAMES -vo pnm -ao null -quiet \
	| grep ^VIDEO | sed 's/^.*\ \([0-9]*\.[0-9]*\)\ fps.*$/\1/')
echo -e "#include <avr/pgmspace.h>\n\nuint16_t framedelay = 1000 / $FPS;" >$OUTPUT
echo -e "#define FRAMES $FRAMES\n#define PIXELS $PIXELS" >>$OUTPUT
echo "uint8_t frames[FRAMES][PIXELS] PROGMEM = {" >>$OUTPUT
python genframes.py $WIDTH $HEIGHT $PIXELS $FRAMES >>$OUTPUT
echo "};" >>$OUTPUT
cat $OUTPUT
