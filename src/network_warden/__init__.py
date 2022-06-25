"""Welcome to the Network Warden package, designed to help you monitor
your network statistics in a digestible manner!
"""

# Enforce Python version check during package import.
import sys

if sys.version_info < (3, 8):
    raise ImportError("Network Warden does not support Python < 3.8")

# Packages may add whatever they like to this file, but
# should keep this content at the top.
#---------------------------------------------------------------