"""

"""
import json
import logging
from abc import ABC, abstractproperty
from pathlib import Path
from typing import List, Tuple

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
    "View",
    "Look",
    "ViewTransform",
    "NamedTransform"
]

"""----------------------------------------------------------------------------
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
    sdr_video = "sdr-video"  # numeric repr proportional to sdr video signal.
    hdr_video = "hdr-video"  # numeric repr proportional to hdr video signal.
    data = "data"  # A non-color channel. (usually + isdata attribute = true.)


"""----------------------------------------------------------------------------
These classes represent OCIO config components. SOme of them subclass the one
define in the OCIO python package while other are created from scratch.
"""


class BaseOCIOComponent(object):
    """
    Abstract class that all OCIO components should implement.
    """

    def __str__(self) -> str:
        """
        All BaseComponents hould return their name when converted to string.
        """
        return self.name

    @abstractproperty
    def name(self) -> str:
        pass


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


class Colorspace(BaseOCIOComponent, ocio.ColorSpace):
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


class Look(BaseOCIOComponent, ocio.Look):
    @property
    def name(self):
        return self.getName()


class Display(BaseOCIOComponent):

    def __init__(self, name, views=None):
        """

        Args:
            name(str):
            views(list or tuple or set or View): list or tuple of View instances.
        """
        self._name = str()
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

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name_value):
        self._name = name_value

    def validate(self):
        """
        Raise an error if this is not a pontential valid display.
        """

        for view in self.views:
            view.validate()

        return


class View(BaseOCIOComponent):

    def __init__(
            self,
            name,
            colorspace,
            view_transform=None,
            looks=None,
            description=None,
            parents=None,
            rule_name=None
    ):
        """

        Args:
            name(str):
            colorspace(Colorspace or str):
                colorspace or colorspace name.
                you can use the special token <USE_DISPLAY_NAME>
                 (see OCIO doc)
            view_transform(ViewTransform or None):
            looks(List[Tuple[str,Look]] or None):
                list of tuple, each tuple must start with look direction(+/-)
                and the last index is the Look instance itself.

                ex: [ ("+", LooK(A)), ("-", Look(B)) ]

            description(str or None):
            parents(list or tuple or set or Display or None):
            rule_name(str or None)
        """
        self._name = str()
        self.parents = list()
        self.looks = str()

        self.name = name
        self.description = description
        # converting to str should return the object the name
        self.colorspace = str(colorspace) if colorspace else None
        # converting to str should return the object the name
        self.view_transform = str(view_transform) if view_transform else None
        self.rule_name = rule_name

        # pre-format the looks to be added as argument later.
        if looks:
            for index, look in enumerate(looks):
                look_dir = look[0]
                look_instance = look[1]
                str_end = "," if index > 0 else ""
                self.looks += f"{look_dir}{look_instance}{str_end}"

        # apply the parent/children system for Display/View
        if not parents:
            pass
        elif isinstance(parents, (list, tuple, set)):
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

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name_value):
        self._name = name_value

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
        if not self.colorspace:
            raise ValueError(
                f"View <{self.name}> require a colorspace to be specified."
            )

        if isinstance(self.colorspace, ColorspaceDisplay):
            if not self.view_transform:
                raise ValueError(
                    f"View <{self.name}> require a view_transform to be "
                    f"specified as the colorspace <{self.colorspace}>"
                    f"is display-referred."
                )

        if not self.parents:
            raise ValueError(
                f"View <{self.name}> doesn't have any parent."
                f"You need to add it to a Display."
            )

        if self.colorspace == ocio.OCIO_VIEW_USE_DISPLAY_NAME:
            if not self.view_transform:
                raise ValueError(
                    f"View <{self.name}> doesn't have a view_transform "
                    f"defined. You need one as the colorspace used is"
                    f"{ocio.OCIO_VIEW_USE_DISPLAY_NAME}."
                )

        return


class ViewTransform(BaseOCIOComponent, ocio.ViewTransform):
    @property
    def name(self):
        return self.getName()


class NamedTransform(BaseOCIOComponent, ocio.NamedTransform):
    def __init__(
            self,
            name,
            aliases=None,
            family=None,
            description=None,
            categories=None,
            forward_transform=None,
            inverse_transform=None,
            encoding=None
    ):
        """
        A NamedTransform provides a way for config authors to include a set of
        color transforms that are independent of the color space being processed.
        For example a “utility curve” transform where there is no need to
        convert to or from a reference space.

        Args:
            name(str):
            aliases(list of str):
            family(str):
            description(str):
            categories(list of str):
            forward_transform(ocio.Transform):
            inverse_transform(ocio.Transform):
            encoding(str):
        """

        super().__init__(
            name,
            aliases if aliases else list(),
            family,
            description,
            forward_transform,
            inverse_transform,
            categories if categories else list(),
        )
        self.setEncoding(encodig=encoding)
        return

    @property
    def name(self):
        return self.getName()


"""----------------------------------------------------------------------------
These classes doesn't represents any OCIO components but are still required to 
build the OCIO config.
"""


class DiskDependency:
    def __init__(self, path_relative, data, write_encoding="utf-8"):
        """
        Represent some data that must be writen next to the config.ocio.
        Luts are the most common example.

        Should be stored in the config object and written at the same time of
        the config.ocio file.

        The path must be relative to the config.ocio file.

        Args:
            path_relative (str or Path):
            data (str): data to write
            write_encoding (str): python.codecs encoding for write

        """
        self.path_relative = Path(path_relative)
        self.data = data
        self.encoding = write_encoding

    def write(self, path):
        """
        Write to disk.

        Args:
            path(str or Path):

        """

        write_path = Path(path) / self.path_relative
        write_path = write_path.resolve()
        write_path.write_text(self.data, encoding=self.encoding)

        if not write_path.exists():
            raise FileNotFoundError(
                f"The file <{write_path}> doesn't exists on disk while it should."
            )

        logger.info(f"[DiskDependency][write] Finished writing to <{write_path}>")
        return
