from .logger import get_logger, setup_logging
from .helpers import deduplicate_links, normalize_link

__all__ = [
    "setup_logging",
    "get_logger",
    "deduplicate_links",
    "normalize_link",
]

__version__ = "0.0.1"
