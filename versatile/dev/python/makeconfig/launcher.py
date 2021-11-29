"""

"""
import logging
import logging.config
import os

PCKG_ABBR = "mkc"  # package abbreviation

logger = logging.getLogger(f"{PCKG_ABBR}.launcher")


def _configure_logging():
    """
    Configure the python logging module.
    """

    logging_config = {

        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "fmt_standard": {
                "format": (
                    f"[{PCKG_ABBR}][%(levelname)7s] "
                    "%(asctime)s [%(name)38s] //%(message)s"
                )
            }
        },

        "handlers": {
            "hl_console": {
                "level": "DEBUG",
                "formatter": "fmt_standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout"
            },
        },

        "loggers": {
            f"{PCKG_ABBR}": {
                "handlers": [
                    "hl_console",
                ],
                "level": os.environ.get("MCK_LOG_LVL", "DEBUG"),
                "propagate": False
            },
        }
    }

    # register
    logging.config.dictConfig(logging_config)

    return


""" ---------------------------------------------------------------------------

PUBLIC

"""


def setup_logging():
    """ Start the logging system

    Returns:
        None
    """

    _configure_logging()
    logger.info("[setup_logging] Completed.")

    return

