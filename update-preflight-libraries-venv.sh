#!/bin/sh
# Update preflight libraries (pysilfont/glyphsLib from master/main)

# Copyright (c) 2022, SIL International  (http://www.sil.org)
# Released under the MIT License (http://opensource.org/licenses/MIT)
# maintained by Nicolas Spalinger

echo "Which python are we using? and from where?"
which python3
python3 --version

echo "Setting up the virtual environment and entering inside"  
python3 -m venv .venv
source .venv/bin/activate

echo "Installing/Updating pip"
python3 -m pip install --upgrade pip

echo "Populating/updating the prefligth dependencies inside the virtual environment"
python3 -m pip install -e git+https://github.com/silnrsi/pysilfont.git@master#egg=pysilfont git+https://github.com/googlefonts/GlyphsLib.git@main#egg=glyphsLib git+https://github.com/fonttools/ufoLib2.git@master#egg=ufoLib2 git+https://github.com/fonttools/fonttools.git@main#egg=fontTools git+https://github.com/typemytype/glyphConstruction.git@master#egg=glyphConstruction fs mutatorMath defcon fontMath

echo ""
echo "Please check these dependencies have been installed correctly: defcon, fontMath, fontTools, glyphConstruction, glyphsLib, MutatorMath, pysilfont and ufoLib2. Only these are currently needed for preflight."

echo ""
psfversion

echo ""
echo "get inside the virtual environment by typing: source .venv/bin/activate"
echo "then run scripts like ./preflight or preglyphs from the inside"

