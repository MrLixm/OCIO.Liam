"""

"""
import logging

import PyOpenColorIO as ocio

from .. import utils

logger = logging.getLogger("mkc.config.recipe")


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

        self.config = None  # type: ocio.Config
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

        self.cs_ap0 = Colorspace(
            name="ACES2065-1",
            description=ColorspaceDescription(
                transfer_function="linear",
                primaries="ACES2065-1",
                whitepoint="ACES",
                details="ACES reference space. Also AP0.",
            ),
            encoding=Encodings.scene_linear,
            family=Families.aces,
            categories=[Categories.input, Categories.output],
        )
        transform = ocio.GroupTransform(
            [
                ocio.BuiltinTransform(style="UTILITY - ACES-AP0_to_CIE-XYZ-D65_BFD"),
            ]
        )
        self.cs_ap0.setTransform(transform, ocio.COLORSPACE_DIR_TO_REFERENCE)
        self.config.addColorSpace(self.cs_ap0)

        self.cs_ap1 = Colorspace(
            name="ACEScg",
            description=ColorspaceDescription(
                transfer_function="linear",
                primaries="ACEScg",
                whitepoint="ACES",
                details="ACES working space. Also AP1.",
            ),
            encoding=Encodings.scene_linear,
            family=Families.aces,
            categories=[Categories.input, Categories.output, Categories.workspace],
        )
        transform = ocio.GroupTransform(
            [
                ocio.BuiltinTransform(style="UTILITY - ACES-AP1_to_CIE-XYZ-D65_BFD"),
            ]
        )
        self.cs_ap1.setTransform(transform, ocio.COLORSPACE_DIR_TO_REFERENCE)
        self.config.addColorSpace(self.cs_ap1)

        return

    @utils.check_config_init
    def build_roles(self):
        """
        """
        # TODO finish once all colorspaces defined
        self.config.setRole(ocio.ROLE_INTERCHANGE_SCENE, self.cs_ref.name)
        self.config.setRole(ocio.ROLE_INTERCHANGE_DISPLAY, self.cs_ref.name)
        self.config.setRole(ocio.ROLE_SCENE_LINEAR, self.cs_srgb_lin.name)
        self.config.setRole(ocio.ROLE_REFERENCE, self.cs_ref.name)
        self.config.setRole(ocio.ROLE_DATA, self.cs_raw.name)
        self.config.setRole(ocio.ROLE_DEFAULT, self.cs_raw.name)
        self.config.setRole(ocio.ROLE_COLOR_PICKING, self.cs_ref.name)
        self.config.setRole(ocio.ROLE_MATTE_PAINT, self.cs_srgb.name)
        self.config.setRole(ocio.ROLE_TEXTURE_PAINT, self.cs_srgb_lin.name)

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

    @utils.check_config_init
    def add_display(self, name,):
        self.config.addDisplayView(
            display=str,
            view=str,
            colorSpaceName=str,
            look=""
        )
        return
