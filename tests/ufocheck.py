# template config file for local testing of ufos with fontbakery.
# inspired by the DaMa folks' ufo_sources.py 

import os

from fontbakery.callable import check, condition, disable
from fontbakery.message import Message
from fontbakery.callable import FontBakeryExpectedValue as ExpectedValue
from fontbakery.checkrunner import (DEBUG, PASS, INFO, SKIP, WARN, FAIL, ERROR, Section, Profile)
from fontbakery.fonts_profile import profile_factory # NOQA pylint: disable=unused-import
from fontbakery.constants import PriorityLevel


class UFOProfile(Profile):

  def setup_argparse(self, argument_parser):
    """Set up custom arguments needed for this profile."""
    import glob
    import logging
    import argparse

    def get_fonts(pattern):

      fonts_to_check = []
      # use glob.glob to accept *.ufo

      for fullpath in glob.glob(pattern):
        fullpath_absolute = os.path.abspath(fullpath)
        if fullpath_absolute.lower().endswith(".ufo") and os.path.isdir(
            fullpath_absolute):
          fonts_to_check.append(fullpath)
        else:
          logging.warning(
              ("Skipping '{}' as it does not seem "
               "to be valid UFO source directory.").format(fullpath))
      return fonts_to_check

    class MergeAction(argparse.Action):

      def __call__(self, parser, namespace, values, option_string=None):
        target = [item for l in values for item in l]
        setattr(namespace, self.dest, target)

    argument_parser.add_argument(
        'fonts',
        # To allow optional commands like "-L" to work without other input
        # files:
        nargs='*',
        type=get_fonts,
        action=MergeAction,
        help='font file path(s) to check.'
        ' Wildcards like *.ufo are allowed.')

    return ('fonts',)


fonts_expected_value = ExpectedValue(
      'fonts'
    , default=[]
    , description='A list of the ufo file paths to check.'
    , validator=lambda fonts: (True, None) if len(fonts) \
                                    else (False, 'Value is empty.')

)

# ----------------------------------------------------------------------------
# This variable serves as an exportable anchor point, see e.g. the
# Lib/fontbakery/commands/check_ufo_sources.py script.
profile = UFOProfile(
    default_section=Section('Default'),
    iterargs={'font': 'fonts'},
    derived_iterables={'ufo_fonts': ('ufo_font', True)},
    expected_values={fonts_expected_value.name: fonts_expected_value})

register_check = profile.register_check
register_condition = profile.register_condition
# ----------------------------------------------------------------------------

# Our own checks below
# See https://font-bakery.readthedocs.io/en/latest/developer/writing-profiles.html

basic_checks = Section("Basic UFO checks")

@register_condition
@condition
def ufo_font(font):
  import defcon
  return defcon.Font(font)
# We use `check` as a decorator to wrap an ordinary python
# function into an instance of FontBakeryCheck to prepare
# and mark it as a check.
# A check id is mandatory and must be globally and timely
# unique. See "Naming Things: check-ids" below.
@register_check(section=basic_checks)
@check(id='org.sil.software/checks/helloworld')
# This check will run only once as it has no iterable
# arguments. Since it has no arguments at all and because
# checks should be idempotent (and this one is), there's
# not much sense in having it all. It will run once
# and always yield the same result.
def hello_world():
    """Simple "Hello (alphabets of the) World" example."""
    # The function name of a check is not very important
    # to create it, only to import it from another module
    # or to call it directly, However, a short line of
    # human readable description is mandatory, preferable
    # via the docstring of the check.

    # A status of a check can be `return`ed or `yield`ed
    # depending on the nature of the check, `return`
    # can only return just one status while `yield`
    # makes a generator out of it and it can produce
    # many statuses.
    # A status also always must be a tuple of (Status, Message)
    # For `Message` a string is OK, but for unit testing
    # it turned out that an instance of `fontbakery.message.Message`
    # can be very useful. It can additionally provide
    # a status code, better suited to figure out the exact
    # check result.
    yield PASS, 'Hello (alphabets of the) World'



@register_check(section=basic_checks)
@check(
  id = 'org.sil.software/checks/ufo-required-fields'
)
def org_sil_software_checks_required_fields(ufo_font):
  """Check that required fields are present in the UFO fontinfo.

    ufo2ft requires these info fields to compile a font binary:
    unitsPerEm, ascender, descender, xHeight, capHeight and familyName.
    """
  recommended_fields = []

  for field in [
      "unitsPerEm", "ascender", "descender", "xHeight", "capHeight",
      "familyName"
  ]:
    if ufo_font.info.__dict__.get("_" + field) is None:
      recommended_fields.append(field)

  if recommended_fields:
    yield FAIL, f"Required field(s) missing: {recommended_fields}"
  else:
    yield PASS, "Required fields present:unitsPerEm, ascender, descender, xHeight, capHeight and familyName "
