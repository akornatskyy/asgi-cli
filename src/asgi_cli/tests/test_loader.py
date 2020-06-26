import unittest

from asgi_cli.loader import from_string


class LoaderTestCase(unittest.TestCase):
    def test_from_string(self) -> None:
        self.assertRaises(ValueError, lambda: from_string("unknown"))
