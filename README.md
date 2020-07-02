# ASGI CLI

![tests](https://github.com/akornatskyy/asgi-cli/workflows/tests/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/akornatskyy/asgi-cli/badge.svg?branch=master)](https://coveralls.io/github/akornatskyy/asgi-cli?branch=master)
[![pypi version](https://badge.fury.io/py/asgi-cli.svg)](https://badge.fury.io/py/asgi-cli)

Call [ASGI](https://asgi.readthedocs.io/en/latest/index.html)
Python application from command line, just like CURL.

If you’re using this tool, **★Star** this repository to show your interest, please!

## Install

```sh
pip install -U asgi-cli
```

## Usage

```sh
asgi-cli --help
```

```text
usage: asgi-cli [-h] [-V] [-X COMMAND] [-H HEADER] [-d DATA | -F MULTIPART]
                [-I] [-b] [-p] [-n NUMBER] [-v]
                app [url]

positional arguments:
  app                   an application module
  url                   a uniform resource locator or path (default /)

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -X COMMAND, --request COMMAND
                        specify request command to use, e.g. POST (default
                        GET)
  -H HEADER, --header HEADER
                        pass custom header line, e.g. -H='Accept:
                        application/json'
  -d DATA, --data DATA  request body data, e.g. '{"msg":"hello"}', 'msg=hello'
  -F MULTIPART, --form MULTIPART
                        specify HTTP multipart POST data, e.g. name=value or
                        name=@file
  -I, --head            show status and headers only
  -b, --benchmark       issue a number of requests through repeated iterations
                        (reports throughtput and average call time)
  -p, --profile         prints out a report of top 10 functions ordered by
                        internal time, saves to 'stats.cprof' file
  -n NUMBER             a number of requests to issue (default 100K)
  -v, --verbose         make the operation more talkative
```

## Examples

_example.py_:

```python
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
```

Then run the examples:

`asgi-cli example:app` prints response body:

```text
Hello, world!
```

`asgi-cli -v example:app` pretty prints scope and sent messages:

```text
{'scope': {'asgi': {'spec_version': '2.1', 'version': '3.0'},
           'client': ('127.0.0.1', 49327),
           'headers': [(b'accept', b'*/*'),
                       (b'user-agent', b'asgi-cli/0.0.1'),
                       (b'host', b'127.0.0.1:8000')],
           'http_version': '1.1',
           'method': 'GET',
           'path': '/',
           'query_string': b'',
           'raw_path': b'/',
           'root_path': '',
           'scheme': 'http',
           'server': ('127.0.0.1', 8000),
           'type': 'http'}}
{'message': {'headers': [(b'content-length', b'13'),
                         (b'content-type', b'text/html; charset=utf-8')],
             'status': 200,
             'type': 'http.response.start'}}
{'message': {'body': b'Hello', 'type': 'http.response.body'}}
{'message': {'body': b', world!', 'type': 'http.response.body'}}
```

`asgi-cli -b example:app` shows execution stats (runs in 3 iterations, for each iteration displays requests per second and an average call time):

```text
 #1 => 477.74K, 2.09μs
 #2 => 438.12K, 2.28μs
 #3 => 446.90K, 2.24μs
```
