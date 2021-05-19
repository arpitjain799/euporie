# -*- coding: utf-8 -*-
"""Defines custom controls which re-render on resize."""
from __future__ import annotations

from typing import Any, Dict, Optional, Type

from prompt_toolkit.cache import SimpleCache
from prompt_toolkit.layout.controls import GetLinePrefixCallable, UIContent, UIControl

from euporie.render import (
    DataRenderer,
    HTMLRenderer,
    ImageRenderer,
    RichRenderer,
    SVGRenderer,
)
from euporie.text import ANSI


class Control(UIControl):
    """Base class for rich cell output.

    Will re-render it's output when the display is resized. Output is generated by
    `Control.renderer`, and is cached per output size.
    """

    renderer: Type[DataRenderer]

    def __init__(self, data: "Any", render_args: "Optional[Dict]" = None) -> "None":
        """Initalize the control.

        Args:
            data: Raw cell output data
            render_args: Additional keyword arguments to pass to the renderer.
        """
        self.data = data
        if render_args is None:
            render_args = {}
        self.render_args = render_args

        self.renderer_instance = self.renderer.select()
        self.rendered_lines: "list" = []
        self._format_cache: SimpleCache = SimpleCache(maxsize=20)
        self._content_cache: SimpleCache = SimpleCache(maxsize=20)

    def preferred_height(
        self,
        width: "int",
        max_available_height: "int",
        wrap_lines: "bool",
        get_line_prefix: Optional[GetLinePrefixCallable],
    ) -> "int":
        """Returns the number of lines in the rendered content."""
        if not self.rendered_lines:
            self.rendered_lines = self._format_cache.get(
                (width, max_available_height),
                lambda: self.render(width, max_available_height),
            )
        return len(self.rendered_lines)

    def create_content(self, width: "int", height: "int") -> UIContent:
        """Generates rendered output at a given size.

        Args:
            width: The desired output width
            height: The desired output height
        """
        self.rendered_lines = self._format_cache.get(
            (width,),
            lambda: self.render(width, height),
        )

        def get_content() -> Optional[UIContent]:
            if self.rendered_lines is not None:
                return UIContent(
                    get_line=lambda i: ANSI(
                        self.rendered_lines[i]
                    ).__pt_formatted_text__(),
                    line_count=len(self.rendered_lines),
                )
            else:
                return None

        return self._content_cache.get((width,), get_content)

    def render(self, width: "int", height: "int") -> "list[str]":
        """Calls the renderer."""
        result = self.renderer_instance.render(
            self.data, width=width, height=height, render_args=self.render_args
        )
        rendered_lines = result.rstrip().split("\n")
        return rendered_lines


class RichControl(Control):
    """Control for rich renderables."""

    renderer = RichRenderer


class HTMLControl(Control):
    """Control for rendered HTML."""

    renderer = HTMLRenderer


class ImageControl(Control):
    """Control for rendered images."""

    renderer: Type[DataRenderer] = ImageRenderer

    def create_content(self, width: int, height: int) -> UIContent:
        """Additionally cache rendered content by cell obscurity status."""
        cell_obscured = self.render_args["cell"].obscured()
        self.rendered_lines: list = self._format_cache.get(
            (cell_obscured, width),
            lambda: self.render(width, height),
        )

        def get_content() -> UIContent:
            return UIContent(
                get_line=lambda i: ANSI(self.rendered_lines[i]).__pt_formatted_text__(),
                line_count=len(self.rendered_lines),
            )

        return self._content_cache.get((cell_obscured, width), get_content)


class SVGControl(ImageControl, Control):
    """Class for rendered SVG iamges."""

    renderer = SVGRenderer
