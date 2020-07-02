import typing

Scope = typing.Dict[str, typing.Any]
Message = typing.MutableMapping[str, typing.Any]
Receive = typing.Callable[[], typing.Awaitable[Message]]
Send = typing.Callable[[Message], typing.Awaitable[None]]
ASGICallable = typing.Callable[[Scope, Receive, Send], typing.Awaitable[None]]
Headers = typing.List[typing.Tuple[bytes, bytes]]


class Options:
    command: str
    headers_only: bool
    header: typing.List[str]
    data: bytes
    multipart: typing.List[str]
    boundary: bytes
    benchmark: bool
    profile: bool
    number: int
    verbose: bool
    app: str
    url: str
