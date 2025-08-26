"""navspec - A declarative dashboard tool."""

__version__ = "0.1.0"
__author__ = "Boni Dukic"
__email__ = "boni@dukic.dev"

from .config import ConfigManager
from .server import DashboardServer
from .types import DashboardConfig, Category, Link, DashboardMetadata

__all__ = [
    "ConfigManager",
    "DashboardServer", 
    "DashboardConfig",
    "Category",
    "Link",
    "DashboardMetadata",
]
