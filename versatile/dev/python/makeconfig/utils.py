"""

"""
import logging

import colour
import numpy

from . import setup

logger = logging.getLogger("mkc.utils")


def check_config_init(func: classmethod):
    """
    Decorator,
    Raises an error is self.config=None, which mean the
    config has never been built yet.

    Returns:
        function: wrapper function that execute passed func
    """

    def wrapper(*args, **kwargs):

        if not args[0].config:
            raise ValueError(
                "config attribute has never been built yet: "
                "self.config=None"
            )

        func(*args, **kwargs)
        return

    return wrapper


def matrix_3x3_to_4x4(matrix):
    """
    Convert a 3x3 matrix to a 4x4 matrix as such :

    [[ value  value  value  0. ]
     [ value  value  value  0. ]
     [ value  value  value  0. ]
     [ 0.     0.     0.    1. ]]

    Args:
        matrix(numpy.ndarray):

    Returns:
        numpy.ndarray: 4x4 matrix
    """

    output = numpy.append(matrix, [[0], [0], [0]], axis=1)
    output = numpy.append(output, [[0, 0, 0, 1]], axis=0)

    return output


def matrix_format_oneline(matrix):
    """
    Convert the matrix to a one line list (no nested list).

    Args:
        matrix(numpy.ndarray):

    Returns:
        list: matrix as a single depth list.
    """

    output = numpy.concatenate(matrix).tolist()

    return output


def matrix_format_ocio(matrix):
    """
    Format the given 3x3 matrix to an OCIO parameters complient list.

    Args:
        matrix(numpy.ndarray): 3x3 matrix

    Returns:
        list: 4x4 matrix in a single line list.
    """
    return matrix_format_oneline(matrix_3x3_to_4x4(matrix))


def matrix_transform_ocio(source, target):
    """ By given a source and target colorspace, return the corresponding
     colorspace conversion matrix.

     You can use "XYZ" as a source or target.

    Args:
        source(str): source colorspace, use "XYZ" for CIE-XYZ.
        target(str): target colorspace, use "XYZ" for CIE-XYZ.

    Returns:
        list of float: 4x4 matrix in a single line list.
    """

    m1 = colour.chromatically_adapted_primaries(
        colour.RGB_COLOURSPACES["DCI-P3"].primaries,
        colour.RGB_COLOURSPACES["DCI-P3"].whitepoint,
        colour.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['D65'],
        "Bradford"
    )

    if target == "XYZ":
        matrix = colour.RGB_COLOURSPACES[source]  # type: colour.RGB_Colourspace
        matrix = matrix.matrix_RGB_to_XYZ.round(setup.NUM_ROUND)  # type: numpy.ndarray
    elif source == "XYZ":
        matrix = colour.RGB_COLOURSPACES[target]  # type: colour.RGB_Colourspace
        matrix = matrix.matrix_XYZ_to_RGB.round(setup.NUM_ROUND)  # type: numpy.ndarray
    else:
        cs_in = colour.RGB_COLOURSPACES[source]
        cs_out = colour.RGB_COLOURSPACES[target]
        matrix = colour.matrix_RGB_to_RGB(cs_in, cs_out, setup.CAT)

    print(m1)
    return matrix_format_ocio(matrix)