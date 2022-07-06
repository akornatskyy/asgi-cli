import unittest

from asgi_cli.parser import parse_number


class ParserTestCase(unittest.TestCase):
    def test_parse_number(self) -> None:
        for (s, expected) in [
            ("12345", 12345),
            ("12345678901", 12345678901),
            ("1K", 1e3),
            ("25K", 25e3),
            ("1M", 1e6),
            ("10M", 1e7),
        ]:
            self.assertEqual(parse_number(s), expected)

        for s in [
            "1KK",
            "1G",
            "K",
            "M",
        ]:
            self.assertRaises(ValueError, lambda s: parse_number(s), s)
