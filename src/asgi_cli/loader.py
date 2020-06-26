import importlib
import typing

from asgi_cli.typing import ASGICallable


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
