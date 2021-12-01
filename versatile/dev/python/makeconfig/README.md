# makeconfig

A custom python package to make creation of OCIO v2 configuration easier.
Like cooking a cake :)

Most basic way of creating the config :

```py
import makeconfig

makeconfig.cook()
```


## modules

### [./launcher.py](./launcher.py)

logging system, executed first when import the package.

### [./setup.py](./setup.py)

Configuration of the package (name config was not appropriate here :)
Hold variables that can change some behaviours.

### [./utils.py](./utils.py)

Mostly numpy helpers to perform some maths/formating on arrays.

### [./config/cooker.py](./config/cooker.py)

Got what you need to run to build and write the config to disk.
Getting an actual product out of instructions.

### [./config/ingredients.py](./config/ingredients.py)

Custom classes representings OCIO config components.
To write the config in an even more pythonic way.

### [./config/recipes.py](./config/recipes.py)

Construct the ocio configs here.