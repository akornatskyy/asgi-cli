import argparse
import json
import random
import re
import string
import typing

from asgi_cli import __version__
from asgi_cli.typing import Options

RE_NUMBER = re.compile(r"^(\d+)([MK]{0,1})$")


def parse_number(s: str) -> int:
    m = RE_NUMBER.match(s)
    if not m:
        raise ValueError(f"value {s} is not valid")
    n = int(m.group(1))
    multiplier = m.group(2).upper()
    n *= multiplier == "M" and 1000000 or multiplier == "K" and 1000 or 1
    return n


def parse_options(args: typing.List[str]) -> Options:
    parser = argparse.ArgumentParser()
    parser.add_argument("app", help="an application module")
    parser.add_argument(
        "url",
        nargs="?",
        help="a uniform resource locator or path (default /)",
        default="/",
    )
    parser.add_argument(
        "-V", "--version", action="version", version="%(prog)s " + __version__
    )
    parser.add_argument(
        "-X",
        "--request",
        help="specify request command to use, e.g. POST (default GET)",
        dest="command",
    )
    parser.add_argument(
        "-H",
        "--header",
        help="pass custom header line, e.g. -H='Accept: application/json'",
        action="append",
        dest="header",
        default=[],
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-d",
        "--data",
        help="request body data, e.g. '{\"msg\":\"hello\"}', 'msg=hello'",
        dest="data",
        action="append",
        default=[],
    )
    group.add_argument(
        "-F",
        "--form",
        help="specify HTTP multipart POST data, e.g. name=value or name=@file",
        dest="multipart",
        action="append",
        default=[],
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-I",
        "--head",
        help="show status and headers only",
        action="store_true",
        default=False,
        dest="headers_only",
    )
    group.add_argument(
        "-b",
        "--benchmark",
        help="issue a number of requests through repeated iterations "
        "(reports throughtput and average call time)",
        action="store_true",
        default=False,
        dest="benchmark",
    )
    group.add_argument(
        "-p",
        "--profile",
        help="prints out a report of top 10 functions ordered by "
        "internal time, saves to 'stats.cprof' file",
        action="store_true",
        default=False,
        dest="profile",
    )
    parser.add_argument(
        "-n",
        help="a number of requests to issue (default 100K)",
        default="100K",
        dest="number",
    )
    group.add_argument(
        "-v",
        "--verbose",
        help="make the operation more talkative",
        action="store_true",
        default=False,
        dest="verbose",
    )

    options = parser.parse_args(args)
    options.number = parse_number(options.number)
    if options.benchmark and options.multipart:  # pragma: nocover
        parser.error(
            "argument -b/--benchmark: not allowed with argument -F/--form"
        )
        return
    if options.data:
        if options.command is None:
            options.command = "POST"
        data = "&".join(options.data)
        if not has_content_type(options.header):
            content_type = guess_content_type(data)
            options.header.append(f"content-type: {content_type}")
        options.data = data.encode("utf-8")
    elif options.multipart:
        options.command = "POST"
        boundary = "----" + "".join(
            random.choice(string.ascii_letters) for _ in range(12)
        )
        options.boundary = boundary.encode("latin-1")
        options.header.append(
            f"content-type: multipart/form-data; boundary={boundary}"
        )
    else:
        options.data = b""
    return typing.cast(Options, options)


def guess_content_type(data: str) -> str:
    try:
        json.loads(data)
        return "application/json"
    except ValueError:
        return "application/x-www-form-urlencoded"


def has_content_type(headers: typing.List[str]) -> bool:
    for line in headers:
        name, _ = line.split(": ", 1)
        if name.lower() == "content-type":
            return True
    return False
