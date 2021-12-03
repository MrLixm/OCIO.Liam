"""

"""
import json
import logging

import PyOpenColorIO as ocio

logger = logging.getLogger("mkc.config.ingredients")

__all__ = [
    "Families",
    "Categories",
    "Encodings",
    "ColorspaceDescription",
    "Colorspace",
    "ColorspaceDisplay",
    "Display",
    "View"
]

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
    aces = "ACES"


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


class Display:

    def __init__(self, name, views=None):
        """

        Args:
            name(str):
            views(list or tuple or set or View): list or tuple of View instances.
        """

        self.views = list()
        self.name = str(name)

        if isinstance(views, (list, tuple, set)):
            for view in views:
                self.add_view(view=view)
        elif isinstance(views, View):
            self.add_view(view=views)
        else:
            raise TypeError(
                f"Argument <views> is in an unsuported type."
                f"Excpected Union[list,tuple,set,View] got <{type(views)}>."
            )

        return

    def add_view(self, view):
        """ Add a View to this Display.

        Args:
            view(View):
        """
        if view not in self.views:
            self.views.append(view)
            view.add_parent(parent=self)
        return

    def validate(self):
        """
        Raise an error if this is not a pontential valid display.
        """

        for view in self.views:
            view.validate()

        return


class View:

    def __init__(
            self,
            name,
            colorspace=None,
            view_transform=None,
            display_colorspace=None,
            looks=None,
            description=None,
            parents=None,
            rule_name=None
    ):
        """

        Args:
            name:
            colorspace:
            view_transform:
            display_colorspace:
            looks:
            description(str):
            parents(list or tuple or set or Display):
            rule_name(str)
        """
        self.parents = list()

        self.name = name
        self.description = description
        self.colorspace = colorspace
        self.view_transform = view_transform
        self.display_colorspace = display_colorspace
        self.looks = looks
        self.rule_name = rule_name

        if isinstance(parents, (list, tuple, set)):
            for parent in parents:
                self.add_parent(parent=parent)
        elif isinstance(parents, Display):
            self.add_parent(parent=parents)
        else:
            raise TypeError(
                f"Argument <parents> is in an unsuported type."
                f"Excpected Union[list,tuple,set,Display] got <{type(parents)}>."
            )

        return

    @property
    def is_shared_view(self):
        """
        Returns:
            bool: Is the view used by multiple Display ?
        """

        return len(self.parents) > 1

    def add_parent(self, parent):
        """
        Add a Display where this View is used.

        Args:
            parent(Display):
        """
        if parent not in self.parents:
            self.parents.append(parent)
            parent.add_view(view=self)
        return

    def validate(self):
        """
        Raise an error if this is not a pontential valid view.
        """
        return