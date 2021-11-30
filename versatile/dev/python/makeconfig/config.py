"""

"""
import json
import logging

import colour
import PyOpenColorIO as ocio
import numpy

from . import utils
from . import setup

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


""" ---------------------------------------------------------------------------

The actual configs

"""


class Versatile:
    
    name = "Versatile"

    def __init__(self):
        """
        Python object representing an ocio config.

        Call build() to construct the config. If not called the config
        doesn't exists.

        Call validate() to check if the config is malformed.

        Call str() on its instance to get a ready-to-write string.
        """

        self.config = None
        self.colorspaces = list()
        self.displays = list()
        self.views = list()

        return

    def __str__(self):
        return self.config.serialize()
    
    def build(self):
        """
        Create a new config and build its content.
        """

        self.config = ocio.Config()

        self.build_root()
        self.build_colorspaces()
        self.build_display()
        self.build_roles()
        
        return

    @utils.check_config_init
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

    @utils.check_config_init
    def build_colorspaces(self):
        """
        """

        """--------------------------------------------------------------------
        Display Colorspaces
        
        use ColorspaceDisplay() instead of Colorspace()
        """

        # sRGB
        self.cs_srgb = ColorspaceDisplay(
            name="sRGB",
            description=ColorspaceDescription(
                transfer_function="sRGB EOTF",
                primaries="sRGB",
                whitepoint="D65",
                details="sRGB monitor with piecewise EOTF",
            ),
            encoding=Encodings.srd_video,
            family=Families.display,
            categories=[Categories.input, Categories.output],
        )

        transform = ocio.GroupTransform(
            [
                ocio.BuiltinTransform(style="DISPLAY - CIE-XYZ-D65_to_sRGB"),
                ocio.RangeTransform(0, 1, 0, 1)
            ]
        )
        self.cs_srgb.setTransform(transform, ocio.COLORSPACE_DIR_FROM_REFERENCE)
        self.config.addColorSpace(self.cs_srgb)

        # Rec.709
        self.cs_bt709 = ColorspaceDisplay(
            name="Rec.709",
            description=ColorspaceDescription(
                transfer_function="pow(2.4)",
                primaries="BT.709",
                whitepoint="D65",
                details="with BT.1886 transfer-function encoding",
            ),
            encoding=Encodings.srd_video,
            family=Families.display,
            categories=[Categories.output],
        )

        transform = ocio.GroupTransform(
            [
                ocio.BuiltinTransform(style="DISPLAY - CIE-XYZ-D65_to_REC.1886-REC.709"),
                ocio.RangeTransform(0, 1, 0, 1)
            ]
        )
        self.cs_bt709.setTransform(transform, ocio.COLORSPACE_DIR_FROM_REFERENCE)
        self.config.addColorSpace(self.cs_bt709)

        # Apple Display P3
        self.cs_p3_d = ColorspaceDisplay(
            name="Apple Display P3",
            description=ColorspaceDescription(
                transfer_function="sRGB EOTF",
                primaries="DCI-P3",
                whitepoint="D65",
                details="Standard for Apple displays.",
            ),
            encoding=Encodings.srd_video,
            family=Families.display,
            categories=[Categories.output],
        )

        transform = ocio.GroupTransform(
            [
                # DCI-P3 to CIE-XYZ matrix
                ocio.MatrixTransform(
                    utils.matrix_transform_ocio(
                        source="XYZ",
                        target="Display P3"
                    )
                ),
                # sRGB EOTF encoding
                ocio.ExponentWithLinearTransform(
                    [2.4, 2.4, 2.4, 1.0],
                    [0.055, 0.055, 0.055, 0.0],
                    ocio.NEGATIVE_LINEAR,
                    ocio.TRANSFORM_DIR_INVERSE
                ),
                # clamp
                ocio.RangeTransform(0, 1, 0, 1)
            ]
        )
        self.cs_p3_d.setTransform(transform, ocio.COLORSPACE_DIR_FROM_REFERENCE)
        self.config.addColorSpace(self.cs_p3_d)

        # P3-DCI
        self.cs_p3_dci = ColorspaceDisplay(
            name="P3-DCI",
            description=ColorspaceDescription(
                transfer_function="pow(2.6)",
                primaries="DCI-P3",
                whitepoint="DCI-P3",
                details="Gamma 2.6 (DCI white with Bradford adaptation)",
            ),
            encoding=Encodings.srd_video,
            family=Families.display,
            categories=[Categories.output],
        )

        transform = ocio.GroupTransform(
            [
                ocio.BuiltinTransform(style="DISPLAY - CIE-XYZ-D65_to_G2.6-P3-DCI-BFD"),
                ocio.RangeTransform(0, 1, 0, 1)
            ]
        )
        self.cs_p3_dci.setTransform(transform, ocio.COLORSPACE_DIR_FROM_REFERENCE)
        self.config.addColorSpace(self.cs_p3_dci)

        # P3-DCI-D65
        self.cs_p3_dci_d65 = ColorspaceDisplay(
            name="P3-DCI-D65",
            description=ColorspaceDescription(
                transfer_function="pow(2.6)",
                primaries="DCI-P3",
                whitepoint="D65",
                details="For display using a D65 whitepoint instead of DCI-P3",
            ),
            encoding=Encodings.srd_video,
            family=Families.display,
            categories=[Categories.output],
        )

        transform = ocio.GroupTransform(
            [
                ocio.BuiltinTransform(style="DISPLAY - CIE-XYZ-D65_to_G2.6-P3-D65"),
                ocio.RangeTransform(0, 1, 0, 1)
            ]
        )
        self.cs_p3_dci_d65.setTransform(transform, ocio.COLORSPACE_DIR_FROM_REFERENCE)
        self.config.addColorSpace(self.cs_p3_dci_d65)

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
            categories=[Categories.input, Categories.output],
            is_data=True
        )
        self.config.addColorSpace(self.cs_raw)

        self.cs_srgb_lin = Colorspace(
            name="sRGB - linear",
            description=ColorspaceDescription(
                transfer_function="linear",
                primaries="sRGB",
                whitepoint="D65",
                details="With a linear transfer function instead.",
            ),
            encoding=Encodings.scene_linear,
            family=Families.scene,
            categories=[Categories.input, Categories.output, Categories.workspace],
        )
        transform = ocio.MatrixTransform(
            utils.matrix_transform_ocio(
                source="sRGB",
                target="XYZ"
            )
        )
        self.cs_srgb_lin.setTransform(transform, ocio.COLORSPACE_DIR_TO_REFERENCE)
        self.config.addColorSpace(self.cs_srgb_lin)

        return

    @utils.check_config_init
    def build_roles(self):
        """
        """
        # TODO finish once all colorspaces defined
        self.config.setRole(ocio.ROLE_INTERCHANGE_SCENE, self.cs_ref.name)
        self.config.setRole(ocio.ROLE_INTERCHANGE_DISPLAY, self.cs_ref.name)
        self.config.setRole(ocio.ROLE_SCENE_LINEAR, self.cs_ref.name)
        self.config.setRole(ocio.ROLE_REFERENCE, self.cs_ref.name)
        self.config.setRole(ocio.ROLE_DATA, self.cs_raw.name)
        self.config.setRole(ocio.ROLE_DEFAULT, self.cs_raw.name)
        self.config.setRole(ocio.ROLE_COLOR_PICKING, self.cs_ref.name)
        self.config.setRole(ocio.ROLE_MATTE_PAINT, self.cs_ref.name)
        self.config.setRole(ocio.ROLE_TEXTURE_PAINT, self.cs_ref.name)

        return

    @utils.check_config_init
    def build_display(self):

        pass

    @utils.check_config_init
    def validate(self):
        """
        Raise an error if the config is not properly built.
        """
        self.config.validate()
        return

    @utils.check_config_init
    def add_colorspace(self, colorspace):
        """
        overload config.addColorSpace() to perform additional operations.

        Args:
            colorspace(Colorspace):

        """
        self.config.addColorSpace(colorspace)
        self.colorspaces.append(colorspace)

        return

