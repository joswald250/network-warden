"""Welcome to the Network Warden package, designed to help you monitor
your network statistics in a digestible manner!
"""

__all__ = [
    "graph_network",
    "gui",
    "gui_network",
    "gui_settings",
    "network_monitor",
    "helpers",
]

# Enforce Python version check during package import.
import sys

if sys.version_info < (3, 8):
    raise ImportError("Network Warden does not support Python < 3.8")

# Packages may add whatever they like to this file, but
# should keep this content at the top.
#---------------------------------------------------------------

from importlib.resources import files

from network_warden import (
    graph_network,
    gui,
    helpers,
    gui_settings,
    gui_network,
    network_monitor,
)

del sys