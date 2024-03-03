"""
SIL checks <https://software.sil.org/fonts/>
"""
# pylint: disable=line-too-long  # This is data, not code

from fontbakery.prelude import (
    check,
    condition,
    disable,
    ERROR,
    SKIP,
    PASS,
    FAIL,
    FATAL,
    INFO,
    WARN,
    DEBUG,
)
from fontbakery.message import Message
from fontbakery.utils import exit_with_install_instructions
from fontbakery.constants import NameID, PlatformID, WindowsEncodingID, FsSelection
from fontbakery.testable import CheckRunContext, Font



@check(
    id = 'org.sil.software/check/OFL_FAQ'
)
def org_sil_software_OFL_FAQ(fb, folder):
    """Checks presence of current version of the OFL FAQ"""
  fb.new_check("126", "Font folder should contain FONTLOG.txt")
  assertExists(fb, folder, "OFL-FAQ.txt",
               "Font folder lacks a OFL-FAQ file at '{}'",
               "Font folder should contain a 'OFL-FAQ.txt' file.")






@check(
    id="org.sil/check/is_OFL_FAQ_current",
    rationale="Although optional, it's recommended to have the current version of the OFL-FAQ in your font project",
)
def org_sil_check_is_ofl_faq_current(family_directory):
    """Is the OFL FAQ current?"""

    import os
    parent_path = os.path.abspath(os.path.join(family_directory, os.pardir))
    faq_file = os.path.join(parent_path, "OFL-FAQ.txt")
    if not os.path.exists(faq_file):
        yield WARN, Message(
            "OFL-FAQ.txt file not found",
            "The OFL-FAQ.txt file is missing. Although optional, it's recommended to include it in your project. Get the most current version from https://openfontlicense.org",
        )
    else:
        with open(faq_file,'r',encoding='utf-8') as file:
            data = file.read()
            if not "Version 1.1-update7" in data:
                yield WARN, Message(
                    "FAQ is old",
                    "The OFL-FAQ.txt file in this font project folder is not the most current version, get the latest (1.1-update7 from November 2023) from https://openfontlicense.org",
                    )
            else:
                yield PASS, Message("ok", "OFL FAQ is current.")
