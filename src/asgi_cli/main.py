import asyncio
import os
import sys
import typing

from asgi_cli import builder, formatter, loader, parser
from asgi_cli.executor import Executor
from asgi_cli.typing import Options


async def go(args: typing.List[str]) -> int:
    try:
        options: Options = parser.parse_options(args)
        app = loader.from_string(options.app)
        scope = builder.build_scope(options)
        executor = Executor(app, scope, builder.gen_chunks(options))
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
        return 0
    except Exception as err:
        errno: int = getattr(err, "errno", 1)
        msg: str = getattr(err, "message", str(err))
        sys.stderr.write(f"ERR: {msg}\n")
        return errno


def main(args: typing.Optional[typing.List[str]] = None) -> int:
    if args is None:  # pragma: nocover
        args = sys.argv[1:]
    sys.path.extend([os.path.abspath(".")])
    return asyncio.get_event_loop().run_until_complete(go(args))


if __name__ == "__main__":  # pragma: nocover
    sys.exit(main())
