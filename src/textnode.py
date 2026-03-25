from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode(text={self.text}, text_type={self.text_type}, url={self.url})"


def text_node_to_html_node(text_node):

    text_type = text_node.text_type
    text = text_node.text
    url = text_node.url

    if text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text)
    elif text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text)
    elif text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text)
    elif text_type == TextType.CODE:
        return LeafNode(tag="code", value=text)
    elif text_type == TextType.LINK:
        if url is None:
            raise ValueError("TextNode of type LINK must have a URL")
        return LeafNode(tag="a", value=text, props={"href": url})
    elif text_type == TextType.IMAGE:
        if url is None:
            raise ValueError("TextNode of type IMAGE must have a URL")
        return LeafNode(tag="img", value="", props={"src": url, "alt": text})
    else:
        raise ValueError(f"Unsupported TextType: {text_type}")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) == 1:
            new_nodes.append(node)
            continue
        if len(parts) % 2 == 0:
            raise Exception(f"Invalid markdown syntax: unmatched '{delimiter}'")
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes
