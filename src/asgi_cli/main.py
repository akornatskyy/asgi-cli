import asyncio
import os
import sys
import typing

from asgi_cli import builder, formatter, loader, parser
from asgi_cli.executor import Executor
from asgi_cli.typing import Options


async def go(args: typing.List[str]) -> None:
    options: Options = parser.parse_options(args)
    app = loader.from_string(options.app)
    scope = builder.build_scope(options)
    executor = Executor(app, scope, options.data)
    if options.verbose:
        await executor.verbose_call()
    elif options.benchmark:
        await formatter.print_timing(
            options.number, executor.benchmark(options.number)
        )
    elif options.profile:
        stats = await executor.stats(options.number)
        formatter.print_stats(stats)
        stats.dump_stats("stats.cprof")
    elif options.headers_only:
        res = await executor.capture_call()
        formatter.print_headers(res)
    else:
        res = await executor.capture_call()
        formatter.print_body(res)


def main(args: typing.Optional[typing.List[str]] = None) -> int:
    if args is None:  # pragma: nocover
        args = sys.argv[1:]
    sys.path.extend([os.path.abspath(".")])
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait([go(args)]))
    return 0


if __name__ == "__main__":  # pragma: nocover
    sys.exit(main())
