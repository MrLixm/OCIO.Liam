"""

"""
import logging

import PyOpenColorIO as ocio

from . import recipes

logger = logging.getLogger("mkc.config.cooker")


def cook():

    logger.info("[build] Started")
    logger.info(f"Using OCIO version : {ocio.__version__}")

    versatile = recipes.Versatile()
    # versatile.validate()

    logger.debug(
        "\n\n"
        "--- config.ocio -----------------\n\n"
        f"{versatile}"
    )

    return