#!/bin/sh
# Idea from pkgsrc GD 20080916

if  [ ! -d ${HOME}/.blender ]; then
	echo Softlinking ${HOME}/.blender to point to global /usr/share/blender settings.
        mkdir ${HOME}/.blender
        cp -rf /usr/share/blender/scripts ${HOME}/.blender/scripts
        ln -s /usr/share/blender/.Blanguages ${HOME}/.blender/.Blanguages
        ln -s /usr/share/blender/.bfont.ttf ${HOME}/.blender/.bfont.ttf
        #ln -s /usr/share/blender ${HOME}/.blender
fi

# Recreate the $HOME/.blender if there is new version.

exec /usr/bin/blender.exe "$@"
