"""

"""
import json
import logging

import PyOpenColorIO as ocio

logger = logging.getLogger("mkc.config.ingredients")

__all__ = [
    "Families",
    "Categories",
    "Encodings",
    "ColorspaceDescription",
    "Colorspace",
    "ColorspaceDisplay"
]

"""
We defined "data" classes to hold names used in various parameters.
This avoid human-mistakes as typos and give auto-completions to 
see availables options.
"""


class Families:
    """
    arbitrary
    """
    scene = "Scene"
    display = "Display"
    aces = "ACES"


class Categories:
    """
    arbitrary
    """
    input = "input"
    workspace = "workspace"
    output = "output"


class Encodings:
    """
    standard defined in OCIO doc, can add new ones.
    """
    scene_linear = "scene-linear"  # numeric repr proportional to scene luminance.
    display_linear = "display-linear"  # numeric repr proportional to display luminance.
    log = "log"  # numeric repr roughly proportional to the logarithm of scene-luminance
    srd_video = "srd-video"  # numeric repr proportional to sdr video signal.
    hdr_video = "hdr_video"  # numeric repr proportional to hdr video signal.
    data = "data"  # A non-color channel. (usually + isdata attribute = true.)


class ColorspaceDescription:
    """
    Python object to represent the description string used on ocio.ColorSpace.
    Force the addition of colorspace primary informations such as
    transfer-function, primaries and whitepoint.

    finished string look sliek this :
      {
        components: {tf:linear, pm:CIE-XYZ, wp:D65},
        description: The reference colorspace, CIE XYZ with D65 adaptive white point
    }
    """

    def __init__(
            self,
            transfer_function: str,
            primaries: str,
            whitepoint: str,
            details: str
    ):
        self.tf = transfer_function
        self.pm = primaries
        self.wp = whitepoint
        self.txt = details

    def __repr__(self) -> dict:
        return {
            "components": {"tf": self.tf, "pm": self.pm, "wp": self.wp},
            "details": self.txt
        }

    def __str__(self) -> str:
        return str(
            json.dumps(self.__repr__(), indent=4)
        )


class Colorspace(ocio.ColorSpace):
    """
    SuperClass ocio.ColorSpace to add more utility methods.
    Represent a colorspace defined based on the SCENE REFERENCE SPACE

    Args:
        name(str):
        description(ColorspaceDescription):
        encoding(str):
        family(str):
        categories(list):
        is_data(bool):

    """

    ref_space = ocio.REFERENCE_SPACE_SCENE

    def __init__(
            self,
            name,
            description,
            encoding,
            family,
            categories,
            is_data=False,
    ):

        super(Colorspace, self).__init__(referenceSpace=self.ref_space)

        self.setName(name=name)
        self.setDescription(str(description))
        self.setEncoding(encoding)
        self.setFamily(family)
        self.setIsData(is_data)

        for category in categories:
            self.addCategory(category)

        return

    def __str__(self):
        return self.getName()

    @property
    def name(self):
        return self.getName()


class ColorspaceDisplay(Colorspace):
    """
    Superclass Colorspace which istelf superclass  ocio.ColorSpace.
    Represent a colorspace defined based on the DISPLAY REFERENCE SPACE

    Args:
        name(str):
        description(ColorspaceDescription):
        encoding(str):
        family(str):
        categories(list):
        is_data(bool):

    """

    ref_space = ocio.REFERENCE_SPACE_DISPLAY

    # need to re-declare __init__ to get the documentation working :/
    def __init__(self, name, description, encoding, family, categories, is_data=False):
        super().__init__(name, description, encoding, family, categories, is_data)


class Display:

    def __init__(self, name, views):

        self.name = name


class View:

    def __init__(self, name, description=""):

        self.name = name
        self.description = description if description else None
        self.colorspace = colorspace
        self.view_transform = view_transform
        self.display_colorspace = display_colorspace
        self.looks = looks
