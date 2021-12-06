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


def matrix_whitepoint_transform(source_whitepoint,
                                target_whitepoint,
                                transform="Bradford"):
    """ Return the matrix to perform a chromatic adaptation with the given
    parameters.

    Args:
        source_whitepoint(numpy.ndarray): source whitepoint name as xy coordinates
        target_whitepoint(numpy.ndarray): target whitepoint name as xy coordinates
        transform(str): method to use.

    Returns:
        numpy.ndarray: chromatic adaptation matrix from test viewing conditions
         to reference viewing conditions. A 3x3 matrix.
    """

    matrix = colour.adaptation.matrix_chromatic_adaptation_VonKries(
        colour.xy_to_XYZ(source_whitepoint),
        colour.xy_to_XYZ(target_whitepoint),
        transform=transform
    )

    return matrix


def matrix_colorspace_transform(source,
                                target,
                                source_whitepoint=None,
                                target_whitepoint=None):
    """ By given a source and target colorspace, return the corresponding
     colorspace conversion matrix.

     You can use "XYZ" as a source or target.
     In that case it is recommended to pass a whitepoint as source or target
     (depnds what XYZ is) to perform chromatic adaptation.

    Args:
        source(str): source colorspace, use "XYZ" for CIE-XYZ.
        target(str): target colorspace, use "XYZ" for CIE-XYZ.
        source_whitepoint(str): whitepoint name for source,
        target_whitepoint(str): whitepoint name for target,

    Returns:
        numpy.ndarray: 3x3 matrix
    """

    illum_1931 = colour.CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"]

    perform_cat = True if source_whitepoint or target_whitepoint else False

    if target == "XYZ":

        source_cs = colour.RGB_COLOURSPACES[source]  # type: colour.RGB_Colourspace
        matrix = source_cs.matrix_RGB_to_XYZ.round(setup.NUM_ROUND)  # type: numpy.ndarray

        if perform_cat and not target_whitepoint:
            raise ValueError("Please give a target_whitepoint")

    elif source == "XYZ":

        target_cs = colour.RGB_COLOURSPACES[target]  # type: colour.RGB_Colourspace
        matrix = target_cs.matrix_XYZ_to_RGB.round(setup.NUM_ROUND)  # type: numpy.ndarray

        if perform_cat and not source_whitepoint:
            raise ValueError("Please give a source_whitepoint")

    else:

        source_cs = colour.RGB_COLOURSPACES[source]
        target_cs = colour.RGB_COLOURSPACES[target]
        # if perform_cat, we will perform it after, so disable it for this op
        _cat = None if perform_cat else setup.CAT
        matrix = colour.matrix_RGB_to_RGB(source_cs, target_cs, _cat)

    if perform_cat:

        # use the source colorspace whitepoint if not one specified
        source_whitepoint = source_cs.whitepoint_name if not source_whitepoint else source_whitepoint
        # use the target colorspace whitepoint if not one specified
        target_whitepoint = target_cs.whitepoint_name if not target_whitepoint else target_whitepoint

        matrix_cat = matrix_whitepoint_transform(
            source_whitepoint=illum_1931[source_whitepoint],
            target_whitepoint=illum_1931[target_whitepoint],
            transform=setup.CAT
        )

        matrix = numpy.dot(matrix_cat, matrix)

    return matrix