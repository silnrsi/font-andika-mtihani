
Running FontBakery tests
=========================

running manually on generated TTF from the root of the project folder:
fontbakery check-profile tests/ttfcheck.py results/*.ttf --html results/Andika-Mtihani-fontbakery-ttfchech-report.html

running manually on generated TTF from the tests folder:
fontbakery check-profile ttfcheck.py ../results/*.ttf --html ../results/Andika-Mtihani-fontbakery-ttfcheck-report.html

using the ttfcheck smith subcommand as hard-coded in the project wscript:
smith ttfcheck 
(you might need to uncomment it for a local test as it's chained to the alltest target and everything is not in place on the CI yet.
When conventions are agreed upon with we make a generic smith target. We still need a way to only have one report per font, not one for every weight).


