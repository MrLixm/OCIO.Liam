"""

"""
import json
import logging

import PyOpenColorIO as ocio

logger = logging.getLogger("mkc.contents")

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

    def __init__(
            self,
            name,
            description,
            encoding,
            family,
            categories,
            is_data=False
    ):
        """
        SuperClass ocio.ColorSpace to add more utility methods.

        Args:
            name(str):
            description(ColorspaceDescription):
            encoding(str):
            family(str):
            categories(list):
            is_data(bool):

        """

        super(Colorspace, self).__init__(name=name)

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


class Versatile:
    
    name = "Versatile"

    def __init__(self):

        self.config = ocio.Config()

    def __str__(self):
        return self.config.serialize()
    
    def build(self):

        self.build_root()
        self.build_colorspaces()
        self.build_display()
        # self.build_roles()
        
        return

    def build_root(self):
        """
        Build options related to the config itself.
        """
        
        self.config.setVersion(2, 1)
        self.config.setName(self.name)
        self.config.setDescription(
            'A versatile sRGB based configuration for artists.'
        )
        
        return
    
    def build_roles(self):
        """
        """
        # TODO finish once all colorspaces defined
        self.config.setRole(ocio.ROLE_INTERCHANGE_SCENE, self.cs_ref.name)
        self.config.setRole(ocio.ROLE_INTERCHANGE_DISPLAY, self.cs_ref.name)
        self.config.setRole(ocio.ROLE_SCENE_LINEAR, self.cs_ref.name)
        self.config.setRole(ocio.ROLE_REFERENCE, self.cs_ref.name)
        self.config.setRole(ocio.ROLE_DATA, self.cs_ref.cs_raw)
        self.config.setRole(ocio.ROLE_DEFAULT, self.cs_ref.cs_raw)
        self.config.setRole(ocio.ROLE_COLOR_PICKING, self.cs_ref.name)
        self.config.setRole(ocio.ROLE_MATTE_PAINT, self.cs_ref.name)
        self.config.setRole(ocio.ROLE_TEXTURE_PAINT, self.cs_ref.name)

        return

    def build_colorspaces(self):
        """
        """

        """--------------------------------------------------------------------
        Display Colorspaces
        """

        self.cs_srgb = Colorspace(
            name="sRGB",
            description=ColorspaceDescription(
                transfer_function="sRGB EOTF",
                primaries="sRGB",
                whitepoint="D65",
                details="sRGB monitor with piecewise EOTF",
            ),
            encoding=Encodings.srd_video,
            family=Families.display,
            categories=[Categories.input, Categories.output]
        )
        # TODO transforms
        self.config.addColorSpace(self.cs_srgb)

        """--------------------------------------------------------------------
        Colorspaces
        """

        self.cs_ref = Colorspace(
            name="CIE-XYZ-D65",
            description=ColorspaceDescription(
                transfer_function="linear",
                primaries="CIE-XYZ",
                whitepoint="D65",
                details="The reference colorspace, CIE XYZ with D65 adaptive white point",
            ),
            encoding=Encodings.scene_linear,
            family=Families.scene,
            categories=[Categories.input, Categories.workspace]
        )
        self.config.addColorSpace(self.cs_ref)

        self.cs_raw = Colorspace(
            name="Raw",
            description=ColorspaceDescription(
                transfer_function="none",
                primaries="none",
                whitepoint="none",
                details="The No-operation colorspace.",
            ),
            encoding=Encodings.data,
            family=Families.scene,
            categories=[Categories.input, Categories.output]
        )
        self.config.addColorSpace(self.cs_raw)

        return

    def build_display(self):

        pass

    def validate(self):
        """
        Raise an error if the config is not properly built.
        """
        self.config.validate()
        return

