import unittest

from asgi_cli.formatter import format_number


class FormatterTestCase(unittest.TestCase):
    def test_format_number(self) -> None:
        for (number, expected) in [
            (12345678901, "12,345.68M"),
            (1234567890, "1,234.57M"),
            (123456789.1, "123.46M"),
            (12345678.9, "12.35M"),
            (1234567.89, "1.23M"),
            (123456.789, "123.46K"),
            (12345.6789, "12.35K"),
            (1234.56789, "1.23K"),
            (123.456789, "123.46"),
            (12.3456789, "12.35"),
            (1.23456789, "1.23"),
            (0.12345678, "123.46m"),
            (0.01234567, "12.35m"),
            (0.00123456, "1.23m"),
            (0.00012345, "123.45u"),
            (0.00001234, "12.34u"),
            (0.00000123, "1.23u"),
            (-1234.56789, "-1,234.57"),
        ]:
            self.assertEqual(format_number(number), expected)
