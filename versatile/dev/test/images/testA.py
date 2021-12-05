"""
testA

decode and encode a 8bit sRGB image
output should look the same as input
"""
from pathlib import Path

import PyOpenColorIO as ocio
import colour

CONFIG_PATH = Path("../../../config/config.ocio").resolve()
IMG_BOB = Path("./input/img/bob_ross.jpg")
WRITE_ROOT = Path("./output/testA")


def log(message):
    # very advanced logging sytem :)
    print(message)
    return


def apply_op(img, processor):

    cpu = processor.getDefaultCPUProcessor()
    log(
        f"[appy_op] got cpu processor :\n"
        f"  in bitdepth<{cpu.getInputBitDepth()}>\n"
        f"  out bitdepth <{cpu.getOutputBitDepth()}>\n"
        f"  is no-op ? <{cpu.isNoOp()}>\n"
    )

    # apply conversion
    cpu.applyRGBA(img)
    log(f"[appy_op] processor applied.")

    return


def apply_cs_op(img, config, csin, csout):

    processor = config.getProcessor(
        csout,
        csin,
    )
    log(f"[apply_cs_op] processor from <{csin}> to <{csout}>")

    apply_op(img=img, processor=processor)

    return


def apply_display_op(img, config, display, view, direction):

    processor = config.getProcessor(
        ocio.ROLE_SCENE_LINEAR,
        display,
        view,
        direction
    )
    log(f"[apply_display_op] processor from display:<{display}> to view:<{view}>")

    apply_op(img=img, processor=processor)
    return


def get_source():

    # source array
    img = colour.read_image(str(IMG_BOB))
    log(f"[get_source] Image <{IMG_BOB.name}> read :<{img.shape}>")

    return img


def run_versatile():

    loggername = "run_configA"

    log(f"[{loggername}]")

    config = ocio.Config().CreateFromFile(str(CONFIG_PATH))  # type: ocio.Config
    log(f"[{loggername}] Using OCIO config <{config.getName()}>")
    config.validate()
    log(f"[{loggername}] Config validated")

    img = get_source()
    img_out = img.copy()

    apply_cs_op(
        img_out,
        config=config,
        csin="sRGB",
        csout="sRGB - linear"
    )
    apply_display_op(
        img_out,
        config,
        "sRGB",
        "Display",
        ocio.TRANSFORM_DIR_INVERSE
    )

    # write result
    img_out_path = WRITE_ROOT / "bobross.versatile.jpg"
    colour.write_image(
        img_out,
        str(img_out_path),
        method="ImageIO",
        bit_depth='uint8'
    )
    log(f"[{loggername}] Image written to <{img_out_path.resolve()}>")
    log(f"[{loggername}] Finished")
    return


if __name__ == '__main__':

    run_versatile()
    # run_rs()