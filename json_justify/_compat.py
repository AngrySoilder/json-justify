"""
This maintains Compatibility
"""
import sys

if sys.version_info[0] >= 3:
    text_type = str
    string_types = (str,)

else:
    text_type = unicode
    string_types = (basestring,)
