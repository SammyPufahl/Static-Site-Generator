import unittest
from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    text_to_textnodes,
)
from textnode import TextNode, TextType
from inline_markdown import split_nodes_image, split_nodes_link


class TestMarkdownExtraction(unittest.TestCase):

    def test_extract_markdown_images_single(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images("Images: ![one](url1) and ![two](url2)")
        self.assertListEqual([("one", "url1"), ("two", "url2")], matches)

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images("No images here")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_single(self):
        matches = extract_markdown_links("Check [Google](https://google.com)")
        self.assertListEqual([("Google", "https://google.com")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links("Links: [one](url1) and [two](url2)")
        self.assertListEqual([("one", "url1"), ("two", "url2")], matches)

    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links("No links here")
        self.assertListEqual([], matches)

    def test_images_and_links_separated(self):
        text = "![img](img_url) and [link](link_url)"
        self.assertListEqual(extract_markdown_images(text), [("img", "img_url")])
        self.assertListEqual(extract_markdown_links(text), [("link", "link_url")])


class TestSplitNodes(unittest.TestCase):

    def test_split_images_single(self):
        node = TextNode("Here is ![img](url1)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Here is ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "url1"),
            ],
            new_nodes,
        )

    def test_split_images_multiple(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_none(self):
        node = TextNode("No images here", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_single(self):
        node = TextNode("Click [here](url1)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Click ", TextType.TEXT),
                TextNode("here", TextType.LINK, "url1"),
            ],
            new_nodes,
        )

    def test_split_links_multiple(self):
        node = TextNode(
            "Visit [boot dev](https://www.boot.dev) and [youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_links_none(self):
        node = TextNode("No links here", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_non_text_nodes_preserved(self):
        node_img = TextNode("img", TextType.IMAGE, "url1")
        node_link = TextNode("link", TextType.LINK, "url2")
        new_nodes_img = split_nodes_image([node_img])
        new_nodes_link = split_nodes_link([node_link])
        self.assertListEqual([node_img], new_nodes_img)
        self.assertListEqual([node_link], new_nodes_link)


class TestTextToTextNodes(unittest.TestCase):

    def test_text_with_image_and_link(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )
        nodes = text_to_textnodes(text)
        self.assertIn(
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            nodes,
        )
        self.assertIn(TextNode("link", TextType.LINK, "https://boot.dev"), nodes)
        self.assertTrue(
            any(
                n.text.startswith("This is") and n.text_type == TextType.TEXT
                for n in nodes
            )
        )


if __name__ == "__main__":
    unittest.main()
