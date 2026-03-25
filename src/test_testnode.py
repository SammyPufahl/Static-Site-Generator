import unittest
from textnode import TextNode, TextType, split_nodes_delimiter


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

    def test_split_code(self):
        node = TextNode("Here is `code` text", TextType.TEXT)

        result = split_nodes_delimiter([node], "`", TextType.CODE)

        assert result == [
            TextNode("Here is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]

    def test_split_bold_basic(self):
        node = TextNode("This is **bold** text", TextType.TEXT)

        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        assert result == [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

    def test_split_italic_basic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)

        result = split_nodes_delimiter([node], "_", TextType.ITALIC)

        assert result == [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]


if __name__ == "__main__":
    unittest.main()
