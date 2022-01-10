"""Defines commands relating to notebooks."""

import logging

from prompt_toolkit.filters import buffer_has_focus

from euporie.app.current import get_tui_app as get_app
from euporie.commands.registry import add
from euporie.filters import notebook_has_focus

log = logging.getLogger(__name__)


@add(
    keys="c-s",
    filter=notebook_has_focus,
    group="Notebook",
)
def save_notebook() -> "None":
    """Save the current notebook."""
    nb = get_app().notebook
    if nb is not None:
        nb.save()


@add(
    filter=notebook_has_focus,
    group="Cell",
)
def run_all_cells() -> "None":
    """Run or render all the cells in the current notebook."""
    nb = get_app().notebook
    if nb is not None:
        nb.run_all()


@add(
    keys="a",
    filter=notebook_has_focus & ~buffer_has_focus,
    group="Notebook",
)
def add_cell_above() -> "None":
    """Add a new cell above the current."""
    nb = get_app().notebook
    if nb is not None:
        nb.add_cell_above()


@add(
    keys="b",
    filter=notebook_has_focus & ~buffer_has_focus,
    group="Notebook",
)
def add_cell_below() -> "None":
    """Add a new cell below the current."""
    nb = get_app().notebook
    if nb is not None:
        nb.add_cell_below()


@add(
    keys=("d", "d"),
    filter=notebook_has_focus & ~buffer_has_focus,
    group="Notebook",
)
def delete_cell() -> "None":
    """Delete the current cell."""
    nb = get_app().notebook
    if nb is not None:
        nb.delete()


@add(
    keys="x",
    filter=notebook_has_focus & ~buffer_has_focus,
    group="Notebook",
)
def cut_cell() -> "None":
    """Cut the current cell."""
    nb = get_app().notebook
    if nb is not None:
        nb.cut()


@add(
    keys="c",
    filter=notebook_has_focus & ~buffer_has_focus,
    group="Notebook",
)
def copy_cell() -> "None":
    """Copy the current cell."""
    nb = get_app().notebook
    if nb is not None:
        nb.copy()


@add(
    keys="v",
    filter=notebook_has_focus & ~buffer_has_focus,
    group="Notebook",
)
def paste_cell() -> "None":
    """Paste the last copied cell."""
    nb = get_app().notebook
    if nb is not None:
        nb.paste()


@add(
    keys=("I", "I"),
    filter=notebook_has_focus & ~buffer_has_focus,
    group="Notebook",
)
def interrupt_kernel() -> "None":
    """Interrupt the notebook's kernel."""
    nb = get_app().notebook
    if nb is not None:
        nb.interrupt_kernel()


@add(
    keys=("0", "0"),
    filter=notebook_has_focus & ~buffer_has_focus,
    group="Notebook",
)
def restart_kernel() -> "None":
    """Restart the notebook's kernel."""
    nb = get_app().notebook
    if nb is not None:
        nb.restart_kernel()


@add(
    filter=notebook_has_focus & ~buffer_has_focus,
    group="Notebook",
)
def change_kernel() -> "None":
    """Change the notebook's kernel."""
    nb = get_app().notebook
    if nb is not None:
        nb.change_kernel()


@add(
    keys="[",
    filter=notebook_has_focus & ~buffer_has_focus,
    group="Notebook",
)
@add(
    keys="<scroll-up>",
    filter=notebook_has_focus,
    group="Notebook",
)
def scroll_up() -> "None":
    """Scroll the page up a line."""
    nb = get_app().notebook
    if nb is not None:
        nb.page.scroll(1)


@add(
    keys="]",
    filter=notebook_has_focus & ~buffer_has_focus,
    group="Notebook",
)
@add(
    keys="<scroll-down>",
    filter=notebook_has_focus,
    group="Notebook",
)
def scroll_down() -> "None":
    """Scroll the page down a line."""
    nb = get_app().notebook
    if nb is not None:
        nb.page.scroll(-1)


@add(
    keys="{",
    filter=notebook_has_focus & ~buffer_has_focus,
    group="Notebook",
)
def scroll_up_5_lines() -> "None":
    """Scroll the page up 5 lines."""
    nb = get_app().notebook
    if nb is not None:
        nb.page.scroll(5)


@add(
    keys="}",
    filter=notebook_has_focus & ~buffer_has_focus,
    group="Notebook",
)
def scroll_down_5_lines() -> "None":
    """Scroll the page down 5 lines."""
    nb = get_app().notebook
    if nb is not None:
        nb.page.scroll(-5)


@add(
    keys=["home", "c-up"],
    group="Notebook",
    filter=notebook_has_focus & ~buffer_has_focus,
)
def first_child() -> "None":
    """Select the first cell in the notebook."""
    nb = get_app().notebook
    if nb is not None:
        nb.page.selected_index = 0


@add(
    keys="pageup",
    group="Notebook",
    filter=notebook_has_focus & ~buffer_has_focus,
)
def select_5th_previous_cell() -> "None":
    """Go up 5 cells."""
    nb = get_app().notebook
    if nb is not None:
        nb.page.selected_index -= 5


@add(
    keys=["up", "k"],
    group="Notebook",
    filter=notebook_has_focus & ~buffer_has_focus,
)
def select_previous_cell() -> "None":
    """Go up one cell."""
    nb = get_app().notebook
    if nb is not None:
        nb.page.selected_index -= 1


@add(
    keys=["down", "j"],
    group="Navigation",
    filter=notebook_has_focus & ~buffer_has_focus,
)
def next_child() -> "None":
    """Select the next cell."""
    nb = get_app().notebook
    if nb is not None:
        nb.page.selected_index += 1


@add(
    keys="pagedown",
    group="Notebook",
    filter=~buffer_has_focus,
)
def select_5th_next_cell() -> "None":
    """Go down 5 cells."""
    nb = get_app().notebook
    if nb is not None:
        nb.page.selected_index += 5


@add(
    keys=["end", "c-down"],
    group="Notebook",
    filter=notebook_has_focus & ~buffer_has_focus,
)
def select_last_cell() -> "None":
    """Select the last cell in the notebook."""
    nb = get_app().notebook
    if nb is not None:
        nb.page.selected_index = len(list(nb.page.children))
