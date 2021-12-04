"""

"""
import logging
import os
import sys
from pathlib import Path

# register parent dir as package source
mck_dir = Path(__file__).parent
sys.path.append(str(mck_dir))

# configure env before staring makeconfig
os.environ["MKC_LOG_LVL"] = "INFO"  # TODO doesn't work

from Versatile import Versatile

# configure logging
logger = logging.getLogger("create_config")
logger.setLevel(logging.DEBUG)
_handler = logging.StreamHandler()
_handler.setLevel(logging.DEBUG)
_handler.setFormatter(
    logging.Formatter("[versatile][%(levelname)7s] %(asctime)s [%(name)20s] //%(message)s")
)
logger.addHandler(_handler)


def cook():

    versatile = Versatile()
    versatile.validate()

    # logger.debug(
    #     "\n\n"
    #     "--- config.ocio -----------------\n\n"
    #     f"{versatile}"
    # )

    versatile.write_to_disk("../../config/config.ocio")

    return


if __name__ == '__main__':

    cook()