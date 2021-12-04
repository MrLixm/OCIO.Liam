"""

"""

import PyOpenColorIO as ocio

import makeconfig
from makeconfig.config.ingredients import *
from makeconfig import utils


class Versatile(makeconfig.BaseConfig):
    
    name = "Versatile"

    def cook_root(self):

        self.config.setVersion(2, 1)
        self.config.setName(self.name)
        self.config.setDescription(
            'A versatile sRGB based configuration for artists.'
        )

        return

    def cook_colorspaces(self):

        _ = "just to avoid the under being considered as method's docstring"

        """====================================================================
        
        Display Colorspaces
        
        use ColorspaceDisplay() instead of Colorspace()
        
        """

        """____________________________________________________________________

            sRGB

        """
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
        self.add(self.cs_srgb)

        """____________________________________________________________________

            Rec.709

        """
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
        self.add(self.cs_bt709)

        """____________________________________________________________________

            Apple Display P3

        """
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
        _matrix = utils.matrix_colorspace_transform(
            source="XYZ",
            target="Display P3",
            source_whitepoint="D65"
        )
        _matrix = utils.matrix_format_ocio(_matrix)

        transform = ocio.GroupTransform(
            [
                # DCisplay P3 to CIE-XYZ matrix
                ocio.MatrixTransform(_matrix),
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
        self.add(self.cs_p3_d)

        """____________________________________________________________________

            P3-DCI

        """
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
        self.add(self.cs_p3_dci)

        """____________________________________________________________________

            P3-DCI-D65

        """
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
        self.add(self.cs_p3_dci_d65)

        """====================================================================
        
        Colorspaces
        
        """

        """____________________________________________________________________

            CIE-XYZ-D65

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
        self.add(self.cs_ref)

        """____________________________________________________________________

            Raw

        """
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
        self.add(self.cs_raw)

        """____________________________________________________________________

            sRGB - linear

        """
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
        _matrix = utils.matrix_colorspace_transform(
                source="sRGB",
                target="XYZ",
                target_whitepoint="D65"
        )
        _matrix = utils.matrix_format_ocio(_matrix)
        transform = ocio.MatrixTransform(_matrix)
        self.cs_srgb_lin.setTransform(transform, ocio.COLORSPACE_DIR_TO_REFERENCE)
        self.add(self.cs_srgb_lin)

        """____________________________________________________________________
        
            ACES2065-1
            
        """
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
        self.add(self.cs_ap0)

        """____________________________________________________________________
        
            ACEScg

        """
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
        self.add(self.cs_ap1)

    def cook_looks(self):

        return

    def cook_viewtransforms(self):

        self.viewtm_aces = ViewTransform(ocio.REFERENCE_SPACE_SCENE)
        self.viewtm_aces.setName("ACES")
        transform = ocio.GroupTransform(
            [
                ocio.ColorSpaceTransform(
                    src=self.cs_ref.name,
                    dst=self.cs_ap0.name
                ),
                ocio.BuiltinTransform(style="ACES-OUTPUT - ACES2065-1_to_CIE-XYZ-D65 - SDR-VIDEO_1.0"),
            ]
        )
        self.viewtm_aces.setTransform(transform, ocio.VIEWTRANSFORM_DIR_FROM_REFERENCE)
        self.add(self.viewtm_aces)

        return

    def cook_display(self):
        self.view_raw = View("Raw", colorspace=self.cs_raw)
        self.view_disp = View("Display", colorspace=self.cs_raw)
        self.view_test = View("Test", colorspace=self.cs_raw)

        self.dp_srgb = Display(
            "sRGB",
            [self.view_raw, self.view_disp]
        )
        self.dp_p3_d = Display(
            "Apple Display P3",
            [self.view_raw, self.view_disp]
        )
        self.dp_bt709 = Display(
            "Rec.709",
            [self.view_raw, self.view_disp, self.view_test]
        )

        self.add(self.dp_srgb)
        self.add(self.dp_bt709)
        self.add(self.dp_p3_d)

        return

    def cook_roles(self):
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
