MPlayer-LoL shield frame generator
==================================

Using this tool one can convert any video that MPlayer can play into a format that can be displayed as an animation ona LoL shield. MPlayer is a free and open source (GPL licensed) award winning cross-platform media player that supports a wide variety of media formats.

Usage
-----

Modify the INPUT, START and FRAMES variables in the genframes.sh file to the input video, the number of seconds to skip from the beginning of the video, and the number of frames to export respectively. If everything is configured right and all the required software are installed, running ./genframes.sh produces frame.h which contains all the frames from the selected interval of the video and the delay needed to play the video using the original FPS. The example.pde file shows a working example that plays the video residing in the frames.h file in an infinite loop.

Requirements
------------

 - bash
 - MPlayer
 - Python

License
-------

The source code is released under MIT license.
