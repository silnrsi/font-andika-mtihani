#!/bin/sh
# Update preflight libraries (pysilfont/glyphsLib from master/main)

# Copyright (c) 2022, SIL International  (http://www.sil.org)
# Released under the MIT License (http://opensource.org/licenses/MIT)
# maintained by Nicolas Spalinger

echo "Which python are we using? and from where?"
which python3
python3 --version

echo "Installing/Updating pip"
python3 -m pip install --upgrade pip

echo "Setting up the virtual environment and entering inside"  
python3 -m pip install poetry 

echo "Populating/updating the prefligth dependencies inside the virtual environment"
poetry config --local virtualenvs.in-project true
poetry install 
poetry update

echo ""
echo "Please check these dependencies have been installed correctly: defcon, fontMath, fontTools, glyphConstruction, glyphsLib, MutatorMath, pysilfont and ufoLib2. Only these are currently needed for preflight."

echo ""
psfversion

echo ""
echo "get inside the virtual environment by typing: poetry shell"
echo "then run scripts like ./preflight or preglyphs from the inside"

