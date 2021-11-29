# Versatile OCIO configuration

A versatile (who would have guess) OCIO configuration for indivual artists.

- working colorspace is `sRGB - linear`

- reference colorspace is `CIE-XYZ-D65`

## Displays

- sRGB
- Apple Display P3
- Rec.709
- P3-DCI
- P3-DCI-D65

### Views

- Simple display encoding

- ACES 1.0 RRT
- False Color
- Raw

# Development

First draft is manually edited. Python build in the work.

## Good practices

Good practices followed during the development of the configuration.

### Colorspace Description

All colorspaces (display included) description shoudl be formatted as a dictionnary :

```yaml
{
	components: { transfer-function: <value>, primaries: <value>, whitepoint: <value>},
	description: actual textual description
}
```

This makes no doubt of what the source colorspace is.