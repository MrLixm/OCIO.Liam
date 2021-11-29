"""

"""
import logging

import PyOpenColorIO as ocio

from . import config

logger = logging.getLogger("mkc.build")


def build():

    logger.info("[build] Started")
    logger.info(f"Using OCIO version : {ocio.__version__}")

    versatile = config.Versatile()
    versatile.build()
    # versatile.validate()

    logger.debug(
        "\n\n"
        "--- config.ocio -----------------\n\n"
        f"{versatile}"
    )

    return