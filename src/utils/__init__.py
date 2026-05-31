from .config import HEADERS
from .helpers import deduplicate_links
from .logger import get_logger, setup_logging

__all__ = [
    "setup_logging",
    "get_logger",
    "deduplicate_links",
    "HEADERS",
]

__version__ = "0.0.1"
