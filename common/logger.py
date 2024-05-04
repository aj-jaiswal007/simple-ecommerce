import logging.config

import structlog
from structlog.stdlib import BoundLogger

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "default": {
                "level": "INFO",
                "class": "logging.StreamHandler",
            },
            "file": {
                "level": "INFO",
                "class": "logging.handlers.WatchedFileHandler",
                "filename": "test.log",
            },
        },
        "loggers": {
            "": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": True,
            },
        },
    }
)
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)


def get_logger() -> BoundLogger:
    return structlog.get_logger()
