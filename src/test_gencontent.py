import unittest
from gencontent import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_raises_when_no_h1(self):
        markdown = "## Not a title"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extract_title(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_extract_title_strips_whitespace(self):
        markdown = "#   Hello   "
        self.assertEqual(extract_title(markdown), "Hello")


if __name__ == "__main__":
    unittest.main()
