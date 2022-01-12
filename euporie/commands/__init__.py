"""Defines a centralized command system."""

from euporie.commands import (  # search,
    app,
    buffer,
    cell,
    completions,
    config,
    notebook,
    suggestions,
)
from euporie.commands.base import Command
from euporie.commands.registry import add, commands, get

__all__ = [
    "Command",
    "add",
    "get",
    "commands",
    "config",
    "app",
    "buffer",
    "cell",
    "completions",
    "notebook",
    # "search",
    "suggestions",
]
