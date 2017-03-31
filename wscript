#!/usr/bin/python
# this is a smith configuration file

# set the default output folders
out="results"
DOCDIR="documentation"
OUTDIR="installers"
ZIPDIR="releases"
TESTDIR='tests'
TESTRESULTSDIR = 'test-results'
STANDARDS = 'standards'

# set the font name, version, licensing and description
APPNAME="AndikaMtihani"
FILENAMEBASE="AndikaMtihani"
VERSION="5.500"
TTF_VERSION="5.500"
COPYRIGHT="Copyright (c) 2004-2015, SIL International (http://www.sil.org)"
LICENSE='OFL.txt'

DESC_SHORT = "Test font for UFO workflows"
DESC_LONG = """
Andika Mtihani is a Latin script font family for testing UFO-based workflows.
It is not intended to be generally useful as an installable font family, and
may change significantly without notice. It will always be experimental and
may not work as you expect!
"""
DESC_NAME = "AndikaMtihani"
DEBPKG = 'fonts-sil-andikamtihani'

for style in ('-Regular','-Bold','-Italic','-BoldItalic') :
    font(target = FILENAMEBASE + style + '.ttf',
        source = 'source/' + FILENAMEBASE + style + '.ufo',
        version = VERSION,
        license = ofl('Andika'),
        script = 'latn',
        fret = fret(params = '-r'),
        woff = woff()
    )
