import pprint
import typing
from pstats import Stats

from asgi_cli.timing import repeat
from asgi_cli.typing import ASGICallable, Headers, Message, Scope

pp = pprint.PrettyPrinter()


class Response(object):
    def __init__(self) -> None:
        self.status_code: int = 0
        self.headers: Headers = []
        self.chunks: typing.List[bytes] = []

    @property
    def body(self) -> bytes:
        return b"".join(self.chunks)


class Executor(object):
    def __init__(self, app: ASGICallable, scope: Scope, data: bytes) -> None:
        self.app = app
        self.scope = scope
        self.data = data

    def verbose_call(self) -> typing.Awaitable[None]:
        pp.pprint({"scope": self.scope})

        async def receive() -> Message:  # pragma: nocover
            m = {"type": "http.request", "body": self.data}
            pp.pprint({"message": m})
            return m

        async def send(message: Message) -> None:
            pp.pprint({"message": message})

        return self.app(self.scope, receive, send)

    async def capture_call(self) -> Response:
        res = Response()

        async def receive() -> Message:  # pragma: nocover
            return {"type": "http.request", "body": self.data}

        async def send(message: Message) -> None:
            if message["type"] == "http.response.start":
                res.status_code = message["status"]
                res.headers = message["headers"]
            elif message["type"] == "http.response.body":
                # TODO: more_body
                chunk: typing.Optional[bytes] = message.get("body")
                if chunk is not None:
                    res.chunks.append(chunk)

        await self.app(self.scope, receive, send)

        return res

    async def benchmark(self, number: int) -> typing.AsyncIterator[float]:
        app = self.app
        scope = self.scope

        async def asgi_app_caller() -> None:
            async def receive() -> Message:  # pragma: nocover
                return {"type": "http.request", "body": self.data}

            async def send(message: Message) -> None:
                pass

            # shallow copy should be just fine, right?
            await app(scope.copy(), receive, send)

        async for time in repeat(asgi_app_caller, number=number):
            yield time

    async def stats(self, number: int) -> Stats:
        import asyncio
        import cProfile
        import threading

        st = Stats()

        def worker() -> None:
            def f() -> None:
                async def x() -> None:
                    async for r in self.benchmark(number):
                        pass

                loop = asyncio.new_event_loop()
                loop.run_until_complete(x())
                loop.close()

            st.add(cProfile.Profile().runctx("f()", globals(), locals()))

        t = threading.Thread(target=worker)
        t.start()
        t.join()
        return st
