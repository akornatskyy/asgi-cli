import gc
import itertools
import time
import typing


async def timeit(
    f: typing.Callable[[], typing.Awaitable[None]], n: int = 1000000
) -> float:
    it = itertools.repeat(None, n)
    enabled = gc.isenabled()
    gc.disable()
    try:
        s = time.perf_counter()
        for _ in it:
            await f()
        return time.perf_counter() - s
    finally:
        if enabled:
            gc.enable()


async def repeat(
    f: typing.Callable[[], typing.Awaitable[None]],
    repeat: int = 3,
    number: int = 1000000,
) -> typing.AsyncIterator[float]:
    for _ in range(repeat):
        t = await timeit(f, number)
        yield t
