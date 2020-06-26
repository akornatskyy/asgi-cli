import copy
from urllib.parse import unquote, urljoin, urlsplit

from asgi_cli import __version__
from asgi_cli.typing import Options, Scope

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
