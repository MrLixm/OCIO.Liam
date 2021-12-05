# Versatile OCIO configuration

![OCIO version](https://img.shields.io/badge/OCIO%20version-v2-informational)

A versatile (who would have guessed), lightweight (no LUTs)
OCIO configuration for individual artists.

![working colorspace](https://img.shields.io/badge/working%20colorspace-sRGB%20--%20linear-6a54c4)

![reference colorspace](https://img.shields.io/badge/reference%20colorspace-CIE--XYZ--D65-6a54c4)

## Specifications

### Displays

- sRGB
- Apple Display P3
- Rec.709
- P3-DCI
- P3-DCI-D65

### Views

- Simple display encoding
- ACES 1.0 RRT
- Raw

# Development

See [dev](./dev) directory.

Run [create_config.py](./dev/python/create_config.py) to create the config.

The config is defined in [Versatile.py](./dev/python/Versatile.py)

## Environment

Developed on Python 3.6.8.

See [requirements.txt](../requirements.txt) for venv packages.

