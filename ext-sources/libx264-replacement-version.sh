#!/bin/bash
VER="git-2245M"
     echo "#define X264_VERSION \" r$VER\"" >> config.h
API=`grep '#define X264_BUILD' < x264.h | sed -e 's/.* \([1-9][0-9]*\).*/\1/'`
echo "#define X264_POINTVER \"0.$API.$VER\"" >> config.h
