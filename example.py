START = {
    "type": "http.response.start",
    "status": 200,
    "headers": [
        (b"content-length", b"13"),
        (b"content-type", b"text/html; charset=utf-8"),
    ],
}

BODY1 = {"type": "http.response.body", "body": b"Hello"}
BODY2 = {"type": "http.response.body", "body": b", world!"}


async def helloworld(scope, receive, send) -> None:
    await send(START)
    await send(BODY1)
    await send(BODY2)


async def receiver(scope, receive, send) -> None:
    while True:
        try:
            await receive()
        except StopAsyncIteration:
            break
    await send(START)
    await send(BODY1)
    await send(BODY2)


async def handle_404(scope, receive, send):
    await send(
        {
            "type": "http.response.start",
            "status": 404,
            "headers": [],
        }
    )
    await send({"type": "http.response.body"})


routes = {
    "/": helloworld,
    "/receiver": receiver,
}


async def app(scope, receive, send):
    path = scope["path"]
    handler = routes.get(path, handle_404)
    await handler(scope, receive, send)
