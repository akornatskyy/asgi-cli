import os
import sys
import unittest

from asgi_cli.loader import from_string, should_add_to_syspath


class LoaderTestCase(unittest.TestCase):
    def test_should_add_to_syspath(self) -> None:
        self.assertFalse(should_add_to_syspath(""))
        self.assertFalse(should_add_to_syspath("."))
        for path in sys.path:
            self.assertFalse(should_add_to_syspath(path))
        self.assertTrue(should_add_to_syspath(os.path.dirname(__file__)))

    def test_from_string(self) -> None:
        self.assertRaises(ValueError, lambda: from_string("unknown"))
