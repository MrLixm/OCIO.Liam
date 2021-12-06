# makeconfig

A custom python package to make creation of OCIO v2 configuration easier.
Like cooking a cake :)

Most basic way of creating the config :

```python
import makeconfig

# subclass the base class
class YourConfigName(makeconfig.BaseConfig):
	...
```

Then instantiate the subclass and write it :

```python
from X import YourConfigName

config = YourConfigName()
config.validate()
config.write_to_disk("./config.ocio")

```



# modules

## [./makeconfig/launcher.py](./makeconfig/launcher.py)

logging system, executed first when import the package.

## [./makeconfig/setup.py](./makeconfig/setup.py)

Configuration of the package (name config was not appropriate here :)
Hold variables that can change some behaviours.

## [./makeconfig/utils.py](./makeconfig/utils.py)

Mostly Numpy helpers to perform some maths/formatting on arrays.

Also a matrix helper to generate matrix from colorspace conversions.

## [./makeconfig/config/ingredients.py](./makeconfig/config/ingredients.py)

Custom classes representing OCIO config components.
To write the config in an even more pythonic way.

## [./makeconfig/config/recipes.py](./makeconfig/config/recipes.py)

BaseClass for the OCIO config python object.

# Utilisation

Import and subclass `BaseConfig` from [./makeconfig/config/recipes.py](./makeconfig/config/recipes.py)

```python
import makeconfig

class YourConfigName(makeconfig.BaseConfig):
	name = "Your Config Name"
    ...
```

don't forget to first set the class attribute `name`

Then implement all the abstract methods. The under is in the same order they are getting executed. It is important to respect it as you might need colorspaces defined in `cook_colorspaces()` to use in your display's view defined in `cook_display()`

```python
        def cook_root(self):
            pass
        def cook_colorspaces(self):
            pass
        def cook_named_transform(self):
            pass
        def cook_colorspaces_display(self):
            pass
        def cook_looks(self):
            pass
        def cook_viewtransforms(self):
            pass
        def cook_display(self):
            pass
        def cook_roles(self):
            pass
        def cook_misc(self):
            pass

```

And that is all you have to fill to build the config.

## Ingredients

To build the config your going to use the classes defined in [./makeconfig/config/ingredients.py](./makeconfig/config/ingredients.py) . You can safely import all :

```python
from makeconfig.config.ingredients import *
```

or more safely use a namespace

```python
from makeconfig.config import ingredients as igd
```

This will import :

```python
__all__ = [
    "Families",
    "Categories",
    "Encodings",
    "ColorspaceDescription",
    # base ocio components
    "Colorspace",
    "ColorspaceDisplay",
    "Display",
    "View",
    "Look",
    "ViewTransform",
    "NamedTransform",
    # misc
    "DiskDependency"
]
```

The first four ones are just some helpers while the rest all subclass `BaseOCIOComponent` and are the real building blocks. This sub classing allow to use the property `name` and the `__str__` method for all of the components. OCIO syntax using the name to refer to one component to an other we can use python objects and for registering just passing `component.name` or `str(component)` to avoid typos.

*(We will get back on `DiskDependency` later)*

[comment]: # (TODO: finish wip)

