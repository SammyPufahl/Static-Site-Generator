import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):

    def test_eq_identical(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_neq_different_text_type(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_neq_different_url(self):
        node1 = TextNode("Link text", TextType.LINK, url="https://example.com")
        node2 = TextNode("Link text", TextType.LINK, url="https://other.com")
        self.assertNotEqual(node1, node2)

    def test_eq_default_url_none(self):
        node1 = TextNode("No URL", TextType.TEXT)
        node2 = TextNode("No URL", TextType.TEXT)
        self.assertEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()
