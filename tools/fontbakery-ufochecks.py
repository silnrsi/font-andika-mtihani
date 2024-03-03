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


# placeholder for future UFO format-based checks
