#!/usr/bin/python3
# this is a smith configuration file

# set the font name, version, licensing and description
APPNAME = "AndikaMtihani"

DESC_SHORT = "Test font for UFO workflows"
DESC_NAME = "AndikaMtihani"

getufoinfo('source/AndikaMtihani-Regular.ufo')
BUILDLABEL = "alpha"

fontfamily=APPNAME
for dspace in ('Roman', 'Italic'):
    designspace('source/' + fontfamily + dspace + '.designspace',
                target = "${DS:FILENAME_BASE}.ttf",
                pdf = fret(params="-r -oi"),
                woff = woff(),
                version = VERSION,
    )
