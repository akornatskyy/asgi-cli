import typing
from pstats import Stats

from asgi_cli.executor import Response


def format_number(n: float) -> str:
    if n >= 1000000:
        n /= 1000000
        return f"{n:,.2f}M"
    if n >= 1000:
        n /= 1000
        return f"{n:,.2f}K"
    elif n >= 1 or n <= 0:
        return f"{n:,.2f}"
    elif n >= 0.001:
        n = n * 1000.0
        return f"{n:,.2f}m"
    n = n * 1000000.0
    return f"{n:,.2f}μ"


async def print_timing(
    base: int, iterator: typing.AsyncIterator[float]
) -> None:
    i = 1
    async for time in iterator:
        rps = format_number(base / time)
        percall = format_number(time / base)
        print(f" #{i} => {rps}, {percall}s")
        i += 1


def print_headers(res: Response) -> None:
    print(f"HTTP/1.1 {res.status_code}")
    for name, value in res.headers:
        print(f"{name.decode('latin-1')}: {value.decode('latin-1')}")


def print_body(res: Response) -> None:
    body = res.body
    print(body.decode("utf8"))


def print_stats(stats: Stats) -> None:
    stats.strip_dirs().sort_stats("time").print_stats(10)
