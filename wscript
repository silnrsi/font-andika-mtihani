#!/usr/bin/python
# this is a smith configuration file

# set the font name, version, licensing and description
APPNAME = "AndikaMtihani"

DESC_SHORT = "Test font for UFO workflows"
DESC_NAME = "AndikaMtihani"

getufoinfo('source/AndikaMtihani-Regular.ufo')
BUILDLABEL = "alpha"

# hard-coded fontbakery commands for testing
# testCommand('ttfcheck', cmd='${FONTBAKERY} check-profile -v -C -S ../tests/ttfcheck.py ${SRC[0].abspath()} --html ${TGT} 1> /dev/null; true', extracmds=["fontbakery"], shapers=0, ext=".html", coverage="fonts", shell=1, addfontindex='1', fontmode='all')

fontfamily=APPNAME
for dspace in ('Roman', 'Italic'):
    designspace('source/' + fontfamily + dspace + '.designspace',
                target = "${DS:FILENAME_BASE}.ttf",
                pdf = fret(params="-r -oi"),
                woff = woff()
    )
