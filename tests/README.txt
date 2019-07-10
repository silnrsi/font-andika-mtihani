
Running FontBakery tests
=========================

running manually on generated TTF from the root of the project folder:
fontbakery check-profile tests/ttfcheck.py results/*.ttf --html results/Andika-Mtihani-fontbakery-report.html

running manually on generated TTF from the tests folder:
fontbakery check-profile ttfcheck.py ../results/*.ttf --html results/Andika-Mtihani-fontbakery-report.html

using the ttfcheck smith subcommand as hard-coded in the project wscript:
smith ttfcheck 


