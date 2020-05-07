#!/usr/bin/env python
'''Example for making project-specific changes to the standard pysilfont set of Font Bakery ttf checks.
It will start with all the checks normally run by pysilfont's ttfchecks profile then modify as described below'''
__url__ = 'http://github.com/silnrsi/pysilfont'
__copyright__ = 'Copyright (c) 2020 SIL International (http://www.sil.org)'
__license__ = 'Released under the MIT License (http://opensource.org/licenses/MIT)'
__author__ = 'David Raymond'

from silfont.fbtests.ttfchecks import psfcheck_list, make_profile, check, condition, Message, PASS, FAIL, WARN, SKIP

# General settings
psfvariable_font = False  # Set to True for variable fonts, so different checks will be run

# Change the status for two checks
psfcheck_list["com.google.fonts/check/whitespace_glyphnames"]["temp_change_status"] = {
    "FAIL": "WARN", "reason": "Google check does not like Space as a name"}
psfcheck_list["com.google.fonts/check/license/OFL_copyright"]["temp_change_status"] = {"FAIL": "WARN", "reason": "Google does not like OFL copyright format"}

#  Create the fontbakery profile
profile = make_profile(psfcheck_list, variable_font = psfvariable_font)

# Add any project-specific tests

@profile.register_condition()
@condition
def adobe_glyphlist():
  """Get Adobe's glyph list"""
  from csv import reader
  from pkg_resources import resource_filename
  agl = {}

  # When this code is in a proper profile module, we can do the following:
  # CACHED = resource_filename('silfonts', 'data/aglfn.txt.cache')
  # Until then, we need to find the data file the hard way:
  from os.path import relpath, dirname, join
  CACHED = join(relpath(dirname(__file__)), 'glyphlist.txt')

  with open(CACHED) as f:
    for row in reader(f, delimiter=';'):
      if row[0].startswith('#'):
        continue
      (name,usvs) = row
      agl[name] = [int(usv,16) for usv in usvs.split()]

  return agl

@profile.register_condition()
@condition
def adobe_aglfn():
  """Get Adobe's glyph list for new fonts"""
  from csv import reader
  from pkg_resources import resource_filename
  aglfn = {}

  # When this code is in a proper profile module, we can do the following:
  # CACHED = resource_filename('silfonts', 'data/aglfn.txt.cache')
  # Until then, we need to find the data file the hard way:
  from os.path import relpath, dirname, join
  CACHED = join(relpath(dirname(__file__)), 'aglfn.txt')

  with open(CACHED) as f:
    content = reader(f, delimiter=';')
    for row in content:
      if row[0].startswith('#'):
        continue
      (usv,name,comment) = row
      aglfn[name] = int(usv,16)

  return aglfn

@profile.register_check
@check(
  id = 'org.sil.software/check/aglfn_compliant',
  conditions = ['adobe_glyphlist','adobe_aglfn'],
  rationale = '''Non-component glyph names must be agl-compliant and should be aglfn-compliant.
  Assumes glyph names are well-formed -- can be verified
  with 'com.google.fonts/check/valid_glyphnames'.
  Permits glyphnames to start with '_' (normally used
  for glyph components) as long as unencoded.'''
)
def org_sil_software_check_aglfn_compliant(ttFont, adobe_glyphlist, adobe_aglfn):
  "Glyph names are agl-compliant"
  # FIXME: Just because a glyphname starts with "_" doesn't mean it is used only as
  # a component. It would be better to find all the component glyphs by algorithm.
  # This would require searching cmap and GSUB tables to get a list of glyphs that
  # we know are *not* components; everything else is.
  
  # Create inverse cmap, used to determine if glyphs are encoded in this font
  cmap_gname2usv = {gname: usv for usv, gname in ttFont.getBestCmap().items()}

  from fontbakery.utils import pretty_print_list
  if ttFont.sfntVersion == b'\x00\x01\x00\x00' and ttFont.get(
      "post") and ttFont["post"].formatType == 3.0:
    yield SKIP, ("TrueType fonts with a format 3.0 post table contain no"
                 " glyph names.")

  import re
  # match names like 'u12345' or 'uni1234abcd'
  uniRE = re.compile(r'(?:u([0-9a-fA-F]{4,6})$)|(?:uni((?:[0-9a-fA-F]{4,4})+)$)')

  # Possible status bits from agl_decode:
  AGL_OK = 0
  NON_AGL = 0x1     # One ore more components in the glyphname are not agl
  NON_AGLFN = 0x2   # One ore more components in the glyphname are not aglfn

  def agl_decode(glyphname):
    """ parses a glyph name and returns a tuple containing a
    status value and a tuple of USVs (some of which could be None)"""
    usvs = []
    status = AGL_OK
    # discard everything after first '.':
    gn = glyphname.split('.', maxsplit=1)[0]  
    # Split into components, if any, and process each:
    for c in gn.split('_'):
      m = uniRE.match(gn)
      if m:
        if m.group(1):
          usvs.append(int(m.group(1),16))
        if m.group(2):
          for i in range(0, len(m.group(2)), 4):
            usvs.append(int(m.group(2)[i:i+4],16))
      elif gn not in adobe_glyphlist:
        status |= NON_AGL
        usvs.append(None)
      else:
        usvs.extend(adobe_glyphlist[c])
        if c not in adobe_aglfn:
          status |= NON_AGLFN
    return (status,usvs)

  passed = True
  component_names_unencoded = []  # These cause WARN
  component_names_encoded = []    # These cause FAIL
  non_agl_names_unencoded = []    # These cause WARN
  non_agl_names_encoded = []      # These cause FAIL
  non_aglfn_names = []            # These cause WARN
  misencoded_glyphs = []          # name is agl but encoded differently than agl; causes FAIL
  for glyphname in ttFont.getGlyphOrder():
    if glyphname in [".null", ".notdef", "nonmarkingreturn", "tab", ".ttfautohint"]:
      # These names are explicit exceptions in the glyph naming rules
      continue
    if glyphname.startswith('_'):
      # Relaxed rules for glyph names starting with '_' normally used as glyph components
      # but they must not be encoded.
      if glyphname in cmap_gname2usv:
        component_names_encoded.append(glyphname)
        passed = False
      else:
        component_names_unencoded.append(glyphname)
      continue
    status,usvs = agl_decode(glyphname)
    if status & NON_AGLFN:
      non_aglfn_names.append(glyphname)
    if status & NON_AGL:
      if len(usvs) == 1 and glyphname in cmap_gname2usv:
        non_agl_names_encoded.append(glyphname)
      else:
        non_agl_names_unencoded.append(glyphname)
    else:
      if len(usvs) == 1 and glyphname in cmap_gname2usv and cmap_gname2usv[glyphname] != usvs[0]:
        misencoded_glyphs.append(glyphname)
    if status:
      passed = False

  if len(component_names_unencoded):
    yield WARN, \
          Message('bad_glyphname',
                  f'Glyph names should not start with underscore ("_") unless they never'
                  f' directly enter the glyph stream (for example are used only as component glyphs).' 
                  f' The following glyph names start with "_" but, because they are not encoded,'
                  f' are assumed to be used only as component glyphs: {pretty_print_list(component_names_unencoded)}.')
  if len(component_names_encoded):
    yield FAIL, \
          Message('bad_glyphname',
                  f'Glyph names should not start with underscore ("_") unless they never'
                  f' directly enter the glyph stream (for example are used only as component glyphs).' 
                  f' The following glyph names start with "_" but, because they are encoded,'
                  f' cannot be assumed to be used only as component glyphs: {", ".join(component_names_encoded)}.')
  if len(non_aglfn_names):
    yield WARN, \
          Message('bad_glyphname',
                  f'The following glyph names, though recognized by the Adobe Glyph List algorithm,' 
                  f' are not recommended for use in new fonts: {", ".join(non_aglfn_names)}.')
  if len(non_agl_names_unencoded):
    yield WARN, \
          Message('bad_glyphname',
                  f'The following unencoded glyphs have names that will not be recognized by the'
                  f' Adobe Glyph List algorithm. These names should be changed unless the glyphs'
                  f' never directly enter the glyph stream (for example are used only as component'
                  f' glyphs): {", ".join(non_agl_names_unencoded)}.')
  if len(non_agl_names_encoded):
    yield FAIL, \
          Message('bad_glyphname',
                  f'The following encoded glyphs have names that will not be recognized by the'
                  f' Adobe Glyph List algorithm. These names should be changed to be AGL-compliant:'
                  f' {", ".join(non_agl_names_encoded)}.')
  if len(misencoded_glyphs):
    yield FAIL, \
          Message('bad_encoding',
                  f'The following glyph names will be recognized by the Adobe Glyph List algorithm'
                  f' as a different codepoint than is indicated in the cmap: {", ".join(misencoded_glyphs)}.')
  if passed:
    t =  ' non-component '  if len(component_names_unencoded) else ' '
    yield PASS, f'All{t}glyph names compliant with Adobe Glyph List for New Fonts'
