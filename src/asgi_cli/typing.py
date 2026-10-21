import typing

Scope = dict[str, typing.Any]
Message = typing.MutableMapping[str, typing.Any]
Receive = typing.Callable[[], typing.Awaitable[Message]]
Send = typing.Callable[[Message], typing.Awaitable[None]]
ASGICallable = typing.Callable[[Scope, Receive, Send], typing.Awaitable[None]]
Headers = list[tuple[bytes, bytes]]


class Options:
    method: str
    app_dir: str
    headers_only: bool
    header: list[str]
    data: bytes
    multipart: list[str]
    boundary: bytes
    root_path: str
    benchmark: bool
    profile: bool
    number: int
    verbose: bool
    app: str
    url: str
