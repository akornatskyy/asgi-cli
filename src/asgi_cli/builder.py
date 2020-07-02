import copy
import typing
from mimetypes import guess_type
from urllib.parse import unquote, urljoin, urlsplit

from asgi_cli import __version__
from asgi_cli.typing import Message, Options, Scope

default_port = {"http": 80, "https": 443}
base_url: str = "http://127.0.0.1:8000"
default_scope: Scope = {
    "type": "http",
    "asgi": {"version": "3.0", "spec_version": "2.1"},
    "http_version": "1.1",
    "client": ("127.0.0.1", 49327),
    "root_path": "",
    "headers": [
        (b"accept", b"*/*"),
        (b"user-agent", b"asgi-cli/" + __version__.encode("latin-1")),
    ],
}


def build_scope(options: Options) -> Scope:
    scope: Scope = copy.deepcopy(default_scope)
    if options.headers_only:
        if not options.command:
            options.command = "HEAD"

    scope["method"] = (options.command or "GET").upper()

    for line in options.header:
        name, value = line.encode("latin-1").split(b": ", 1)
        scope["headers"].append((name.lower(), value))

    url = urljoin(base_url, options.url)
    scheme, netloc, path, query, _ = urlsplit(url)
    scope["scheme"] = scheme or "http"
    if ":" in netloc:
        host, sport = netloc.split(":", 1)
        port = int(sport)
    else:
        host = netloc
        port = default_port[scheme]
    scope["server"] = (host, port)
    scope["headers"].append((b"host", netloc.encode("latin-1")))
    scope["raw_path"] = urljoin(path, query).encode()
    scope["path"] = unquote(path)
    scope["query_string"] = query.encode()
    return scope


async def gen_chunks(options: Options) -> typing.AsyncIterator[Message]:
    if not options.multipart:
        yield {"type": "http.request", "body": options.data}
        return
    boundary = b"--" + options.boundary
    for multipart in options.multipart:
        name, value = multipart.split("=", 1)
        if value.startswith("@"):
            fn = value[1:]
            mime_type, _ = guess_type(fn)
            if not mime_type:
                mime_type = "application/octet-stream"
            yield {
                "type": "http.request",
                "more_body": True,
                "body": b"".join(
                    (
                        boundary,
                        b"\r\n" b'Content-Disposition: form-data; name="',
                        name.encode("utf-8"),
                        b'"; filename="',
                        fn.encode("utf-8"),
                        b'"\r\n' b"Content-Type: ",
                        mime_type.encode("latin-1"),
                        b"\r\n\r\n",
                    )
                ),
            }
            f = open(fn, mode="rb")
            while True:
                data = f.read(1024)
                if not data:
                    break
                yield {
                    "type": "http.request",
                    "more_body": True,
                    "body": data,
                }
            f.close()
            yield {
                "type": "http.request",
                "more_body": True,
                "body": b"\r\n",
            }
        else:
            yield {
                "type": "http.request",
                "more_body": True,
                "body": b"".join(
                    (
                        boundary,
                        b'\r\nContent-Disposition: form-data; name="',
                        name.encode("utf-8"),
                        b'"\r\n\r\n',
                        value.encode("utf-8"),
                        b"\r\n",
                    )
                ),
            }
    yield {"type": "http.request", "body": boundary + b"--"}
