"""Define commands at the application level."""

import logging
from functools import partial
from typing import TYPE_CHECKING

from prompt_toolkit.filters import Condition, buffer_has_focus
from pygments.styles import get_all_styles  # type: ignore

from euporie.app.current import get_tui_app as get_app
from euporie.commands.registry import add
from euporie.config import config

if TYPE_CHECKING:
    from prompt_toolkit.enums import EditingMode

log = logging.getLogger(__name__)


@add(
    keys="l",
    filter=~buffer_has_focus,
    group="Config",
    toggled=Condition(lambda: config.line_numbers),
)
def show_line_numbers() -> "None":
    """Toggle the visibility of line numbers."""
    config.toggle("line_numbers")


@add(
    filter=~buffer_has_focus,
    group="Config",
)
def switch_background_pattern() -> "None":
    """Switch between different background patterns."""
    config.toggle("background_pattern")


@add(
    filter=~buffer_has_focus,
    group="Config",
    toggled=Condition(lambda: config.show_cell_borders),
)
def show_cell_borders() -> "None":
    """Toggle the visibility of the borders of unselected cells."""
    config.toggle("show_cell_borders")


@add(
    keys="w",
    filter=~buffer_has_focus,
    group="Config",
    toggled=Condition(lambda: config.expand),
)
def use_full_width() -> "None":
    """Toggle whether cells should extend across the full width of the screen."""
    config.toggle("expand")


@add(
    title="Completions as you type",
    filter=~buffer_has_focus,
    toggled=Condition(lambda: bool(config.autocomplete)),
)
def autocomplete() -> "None":
    """Toggle whether completions should be shown automatically."""
    config.toggle("autocomplete")


@add(
    title="Suggest lines from history",
    group="Config",
    toggled=Condition(lambda: bool(config.autosuggest)),
)
def autosuggest() -> "None":
    """Toggle whether to suggest line completions from the kernel's history."""
    config.toggle("autosuggest")


@add(
    title="Run cell after external edit",
    group="Config",
    toggled=Condition(lambda: bool(config.run_after_external_edit)),
)
def run_after_external_edit() -> "None":
    """Toggle whether cells should run automatically after editing externally."""
    config.toggle("run_after_external_edit")


@add(
    group="Config",
    toggled=Condition(lambda: bool(config.show_status_bar)),
)
def show_status_bar() -> "None":
    """Toggle the visibility of the status bar."""
    config.toggle("show_status_bar")


def set_edit_mode(edit_mode: "EditingMode") -> "None":
    """Set the editing mode key-binding style."""
    get_app().set_edit_mode(edit_mode)


for choice in config.choices("edit_mode"):
    add(
        name=f"set-edit-mode-{choice.lower()}",
        title=choice.title(),
        description=f"Set the editing mode key-binding style to '{choice}'.",
        toggled=Condition(
            partial(lambda x: config.edit_mode == x, choice),
        ),
    )(partial(set_edit_mode, choice))


def update_color_scheme(choice: "str") -> "None":
    """Updates the application's style."""
    get_app().update_style(color_scheme=choice)


for choice in config.choices("color_scheme"):
    add(
        name=f"set-color-scheme-{choice.lower()}",
        title=choice.title(),
        description=f"Set the color scheme to '{choice}'.",
        toggled=Condition(
            partial(lambda x: config.color_scheme == x, choice),
        ),
    )(partial(update_color_scheme, choice))


def update_syntax_theme(choice: "str") -> "None":
    """Updates the application's syntax highlighting theme."""
    get_app().update_style(pygments_style=choice)


for choice in sorted(get_all_styles()):
    add(
        name=f"set-syntax-theme-{choice.lower()}",
        title=choice,
        description=f"Set the syntax highlighting theme to '{choice}'.",
        toggled=Condition(
            partial(lambda x: config.syntax_theme == x, choice),
        ),
    )(partial(update_syntax_theme, choice))
