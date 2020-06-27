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


async def app(scope, receive, send) -> None:
    await send(START)
    await send(BODY1)
    await send(BODY2)
