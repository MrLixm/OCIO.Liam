"""

"""

import unittest


from makeconfig import utils


class Tester01(unittest.TestCase):

    def test_matrix_colorspace_transform(self):

        utils.matrix_colorspace_transform(
            "sRGB",
            "XYZ"
        )
        utils.matrix_colorspace_transform(
            "XYZ",
            "sRGB"
        )
        utils.matrix_colorspace_transform(
            "sRGB",
            "ACEScg"
        )
        # XYZ with CAT
        utils.matrix_colorspace_transform(
            "sRGB",
            "XYZ",
            target_whitepoint="D65"
        )
        self.assertRaises(
            ValueError,
            utils.matrix_colorspace_transform,
            "sRGB",
            "XYZ",
            source_whitepoint="D65"
        )
        utils.matrix_colorspace_transform(
            "XYZ",
            "sRGB",
            source_whitepoint="D65"
        )
        self.assertRaises(
            ValueError,
            utils.matrix_colorspace_transform,
            "XYZ",
            "sRGB",
            target_whitepoint="D65"
        )
        utils.matrix_colorspace_transform(
            "sRGB",
            "XYZ",
            source_whitepoint="D60",
            target_whitepoint="D65"
        )
        utils.matrix_colorspace_transform(
            "XYZ",
            "sRGB",
            source_whitepoint="D60",
            target_whitepoint="D65"
        )
        # RGB 2 RGB with aditional CAT
        utils.matrix_colorspace_transform(
            "sRGB",
            "ACEScg",
            target_whitepoint="D65"
        )
        utils.matrix_colorspace_transform(
            "sRGB",
            "ACEScg",
            source_whitepoint="D60",
            target_whitepoint="D65"
        )

        print("[test_matrix_colorspace_transform] Finished")
        return


if __name__ == '__main__':

    unittest.main()