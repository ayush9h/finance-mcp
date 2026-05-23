import logging
import sys
import structlog


class ColoredFormatter(logging.Formatter):

    COLORS = {
        "DEBUG": "\033[36m",
        "INFO": "\033[32m",
        "WARNING": "\033[33m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[35m",
    }

    RESET = "\033[0m"

    def format(self, record):

        color = self.COLORS.get(record.levelname, self.RESET)

        message = super().format(record)

        return f"{color}{message}{self.RESET}"


def setup_logging(log_level: str = "INFO"):

    console_handler = logging.StreamHandler(sys.stdout)

    console_handler.setFormatter(ColoredFormatter("%(message)s"))

    root_logger = logging.getLogger()

    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Remove duplicate handlers
    root_logger.handlers.clear()

    root_logger.addHandler(console_handler)

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.dev.ConsoleRenderer(colors=True),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str = __name__):
    return structlog.get_logger(name)
