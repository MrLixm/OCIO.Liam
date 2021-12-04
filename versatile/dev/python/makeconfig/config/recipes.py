"""

"""
from abc import ABC, abstractmethod
import logging
from pathlib import Path

import PyOpenColorIO as ocio

from .ingredients import *
from .. import utils

logger = logging.getLogger("mkc.config.recipe")


class BaseConfig(ABC):
    
    name = ""

    def __init__(self):
        """
        Python object representing an ocio config.

        Call cook() to build the config. If not called the config
        doesn't exists.

        Call validate() to check if the config is malformed.

        Call str() on this instance to get a ready-to-write string.
        """

        self.config = ocio.Config()
        self.colorspaces = list()
        self.displays = list()
        self.looks = list()
        self.viewtransforms = list()
        self.disk_dependencies = list()

        # start building the config
        self.cook()  # has to be first
        self.bake()

        return

    def __str__(self):
        """
        Returns:
            str: ready-to-write .ocio file content
        """
        return self.config.serialize()

    def add(self, component):
        """
        Add an object to the config and let it guess how it should add it.
        Objects is actually stored in a list , it is only added to the
        config when bake() is called.

        Args:
            component(any):
        """

        if isinstance(component, Display):
            self.displays.append(component)
            logger.debug(
                f"[{self.__class__.__name__}][add] added Display <{component}>"
            )
        elif isinstance(component, (Colorspace, ColorspaceDisplay)):
            self.colorspaces.append(component)
            logger.debug(
                f"[{self.__class__.__name__}][add] added Colorspace <{component}>"
            )
        elif isinstance(component, Look):
            self.looks.append(component)
            logger.debug(
                f"[{self.__class__.__name__}][add] added Look <{component}>"
            )
        elif isinstance(component, ViewTransform):
            self.viewtransforms.append(component)
            logger.debug(
                f"[{self.__class__.__name__}][add] added ViewTransform <{component}>"
            )
        else:
            raise TypeError(
                "<component> is not from a supported type."
                "Excpected Union[Display, Colorspace, ColorspaceDisplay, Look]"
                f", got <{type(component)}>"
            )

        return
    
    def bake(self):
        """
        Bake the various attributes holded by the class instance to the actual
        config (self.config)
        """

        for colorspace in self.colorspaces:
            self.config.addColorSpace(colorspace)

        for display in self.displays:
            display.validate()

            for view in display.views:

                if view.is_shared_view:
                    # this mean we will add the same view multiple times but
                    # not an issue as it overwrite the previous one.
                    self.config.addSharedView(
                        view=view.name,
                        viewTransformName=view.view_transform,
                        colorSpaceName=view.colorspace,
                        looks=view.looks,
                        ruleName=view.rule_name,
                        description=view.description
                    )
                    # this one tho, will raise an error if you add 2 time the
                    # same view.
                    try:
                        self.config.addDisplaySharedView(
                            display.name,
                            view.name
                        )
                    except Exception as excp:
                        logger.debug(
                            f"[{self.__class__.__name__}][bake] Can't perform"
                            f"self.config.addDisplaySharedView(): {excp}"
                        )

                else:
                    self.config.addDisplayView(
                        display.name,
                        view=view.name,
                        viewTransform=view.view_transform,
                        displayColorSpaceName=view.colorspace,
                        looks=view.looks,
                        ruleName=view.rule_name,
                        description=view.description
                    )

                continue

            continue

        for look in self.looks:
            self.config.addLook(look)

        for viewtransform in self.viewtransforms:
            self.config.addViewTransform(viewtransform)

        logger.debug(
            f"[{self.__class__.__name__}][bake] Finished"
        )
        return

    def cook(self):
        """
        Create a new config and build its content.
        This reset any change done to self.config.
        """

        # make sure the config is reset by creating a new instance
        self.config = ocio.Config()

        # ! Order is important !
        self.cook_root()
        self.cook_colorspaces()
        self.cook_looks()
        self.cook_viewtransforms()
        self.cook_display()
        self.cook_roles()

        return

    @utils.check_config_init
    def validate(self):
        """
        Raise an error if the config is not properly built.
        """
        self.config.validate()
        return

    def write_to_disk(self, write_path):
        """
        Write the config to disk as the config.ocio file.

        Args:
            write_path(str or Path): object representing a path to the
                config.ocio file.

        """

        write_path = Path(write_path).absolute()
        write_path.write_text(self.__str__(), encoding="utf-8")
        logger.info(
            f"[{self.__class__.__name__}][write_to_disk]"
            f"Config written to <{write_path}>"
        )

        # to write luts and other dependencies that have been stored.
        for dependency in self.disk_dependencies:
            dependency.write(write_path)

        logger.info(f"[{self.__class__.__name__}][write_to_disk] Finished.")
        return

    @abstractmethod
    @utils.check_config_init
    def cook_root(self):
        """
        Build options related to the config itself.
        """
        pass

    @abstractmethod
    @utils.check_config_init
    def cook_colorspaces(self):
        """
        Build colorspaces, display colrospaces.
        They should be cook first to be referenced is other components.
        """
        pass

    @abstractmethod
    @utils.check_config_init
    def cook_looks(self):
        """
        Build looks.
        """
        pass

    @abstractmethod
    @utils.check_config_init
    def cook_viewtransforms(self):
        """
        Build viewtransform components.
        """
        pass

    @abstractmethod
    @utils.check_config_init
    def cook_display(self):
        """
        Create Views and Displays.
        Only Displays need to be added to the config as View should be
        parented to a Display.
        """
        pass

    @abstractmethod
    @utils.check_config_init
    def cook_roles(self):
        """
        Build roles in the config. Cook last as colorspaces should alrerady be
        build to be used.
        """
        pass

