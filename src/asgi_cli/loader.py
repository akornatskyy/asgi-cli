import importlib
import os
import sys
import typing

from asgi_cli.typing import ASGICallable


def should_add_to_syspath(app_dir: str) -> bool:
    if not os.path.exists(app_dir):
        return False
    for path in sys.path:
        if os.path.exists(path) and os.path.samefile(app_dir, path):
            return False
    return True


def from_string(import_str: str) -> ASGICallable:
    module_str, _, attrs_str = import_str.partition(":")
    if not module_str or not attrs_str:
        raise ValueError(
            f"import string '{import_str}' "
            "must be in format '<module>:<attribute>'."
        )
    instance = importlib.import_module(module_str)
    for attr_str in attrs_str.split("."):
        instance = getattr(instance, attr_str)
    return typing.cast(ASGICallable, instance)
