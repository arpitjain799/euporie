"""Defines custom controls which re-render on resize."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from prompt_toolkit.cache import SimpleCache
from prompt_toolkit.formatted_text.utils import fragment_list_len
from prompt_toolkit.layout.controls import GetLinePrefixCallable, UIContent, UIControl

from euporie.render import (
    HTMLRenderer,
    ImageRenderer,
    LatexRenderer,
    MarkdownRenderer,
    SVGRenderer,
)
from euporie.text import ANSI

if TYPE_CHECKING:
    from typing import Any, Iterable, List, Optional, Sequence, Type

    from prompt_toolkit.utils import Event

    from euporie.graphics import TerminalGraphic
    from euporie.render import DataRenderer

__all__ = [
    "OutputControl",
    "MarkdownControl",
    "HTMLControl",
    "LatexControl",
    "ImageControl",
    "SVGControl",
]

log = logging.getLogger(__name__)


class OutputControl(UIControl):
    """Base class for rich cell output.

    Will re-render it's output when the display is resized. Output is generated by
    `Control.renderer`, and is cached per output size.
    """

    renderer_class: "Type[DataRenderer]"

    def __init__(
        self,
        data: "Any",
        width: "Optional[int]" = None,
        height: "Optional[int]" = None,
        bg_color: "Optional[str]" = None,
        graphic: "Optional[TerminalGraphic]" = None,
    ) -> "None":
        """Initalize the control.

        Args:
            data: Raw cell output data
            width: The initial height at which to render output
            height: The initial width at which to render output
            bg_color: The background colour to use when renderin this output
            graphic: The terminal graphic linked to this output

        """
        self.data = data
        self.graphic = graphic

        self.renderer: "DataRenderer" = self.renderer_class.select(
            width=width,
            height=height,
            bg_color=bg_color,
            graphic=graphic,
        )
        self.rendered_lines: "list" = []
        self._format_cache: SimpleCache = SimpleCache(maxsize=20)
        self._content_cache: SimpleCache = SimpleCache(maxsize=20)

    @property
    def extra_keys(self) -> "Sequence[Any]":
        """Return extra keys for the output cache.

        Allows subclasses to override cached outputs.

        Returns:
            A sequence of keys

        """
        return ()

    def get_rendered_lines(self, width: "int", height: "int") -> "List[str]":
        """Get rendered lines from the cache, or generate them."""
        return self._format_cache.get(
            (width, *self.extra_keys),
            lambda: self.render(width, height),
        )

    def preferred_width(self, max_available_width: "int") -> "Optional[int]":
        """Returns the width of the rendered content."""
        if self.rendered_lines:
            return max(
                [
                    fragment_list_len(ANSI(line).__pt_formatted_text__())
                    for line in self.rendered_lines
                ]
            )
        return None

    def preferred_height(
        self,
        width: "int",
        max_available_height: "int",
        wrap_lines: "bool",
        get_line_prefix: Optional[GetLinePrefixCallable],
    ) -> "int":
        """Returns the number of lines in the rendered content."""
        if not self.rendered_lines:
            self.rendered_lines = self.get_rendered_lines(width, max_available_height)
        return len(self.rendered_lines)

    def create_content(self, width: "int", height: "int") -> "UIContent":
        """Generates rendered output at a given size.

        Args:
            width: The desired output width
            height: The desired output height

        Returns:
            `UIContent` for the given output size.

        """
        self.rendered_lines = self.get_rendered_lines(width, height)

        def get_content() -> "Optional[UIContent]":
            return UIContent(
                get_line=lambda i: ANSI(self.rendered_lines[i]).__pt_formatted_text__(),
                line_count=len(self.rendered_lines),
            )

        return self._content_cache.get((width, *self.extra_keys), get_content)

    def render(self, width: "int", height: "int") -> "list[str]":
        """Calls the renderer."""
        result = self.renderer.render(self.data, width=width, height=height)
        rendered_lines = result.rstrip("\n").splitlines()
        return rendered_lines


class MarkdownControl(OutputControl):
    """Control for markdown."""

    renderer_class = MarkdownRenderer


class HTMLControl(OutputControl):
    """Control for rendered HTML."""

    renderer_class = HTMLRenderer


class LatexControl(OutputControl):
    """Control for rendered LaTeX."""

    renderer_class = LatexRenderer


class BaseImageControl(OutputControl):
    """Control for rendered raster images."""

    @property
    def extra_keys(self) -> "tuple":
        """Return the obscured status of the image."""
        if self.graphic is not None:
            return (self.graphic.visible(),)
        else:
            return ()

    def get_invalidate_events(self) -> "Iterable[Event[object]]":
        """Return the Window invalidate events."""
        # Whenever the buffer changes, the UI has to be updated.
        if self.graphic is not None:
            yield self.graphic.on_resize
            yield self.graphic.on_move


class ImageControl(BaseImageControl):
    """Control for rendered raster images."""

    renderer_class = ImageRenderer


class SVGControl(BaseImageControl):
    """Class for rendered SVG iamges."""

    renderer_class = SVGRenderer
