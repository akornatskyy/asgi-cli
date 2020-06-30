import unittest

from asgi_cli.main import main


class MainTestCase(unittest.TestCase):
    def test_main(self) -> None:
        main(["example:app"])
        main(["-v", "example:app"])
        main(["-d", "", "example:app"])
        main(["-d", "{}", "example:app"])
        main(["-X", "POST", "-v", "example:app"])
        main(["-X", "POST", "-d", "msg=hello", "example:app"])
        main(["-I", "example:app"])
        main(["-b", "-n", "1K", "example:app"])
        main(["-p", "-n", "1K", "example:app"])
        main(["-H", "Accept: application/json", "example:app"])
        main(["-v", "example:app", "http://example.com/uk/welcome"])
        main(
            [
                "-v",
                "-X",
                "PATCH",
                "-H",
                "Content-Type: application/json",
                "-d",
                "[]",
                "example:app",
                "welcome",
            ]
        )
