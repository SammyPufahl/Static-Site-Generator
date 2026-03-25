from enum import Enum
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks if block.strip()]
    return blocks


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```") and len(lines) >= 3:
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.ULIST
    i = 1
    for line in lines:
        if not line.startswith(f"{i}. "):
            break
        i += 1
    else:
        return BlockType.OLIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    normalized = " ".join(line.strip() for line in block.split("\n"))
    children = text_to_children(normalized)
    return ParentNode("p", children)


def heading_to_html_node(block):
    lines = block.split("\n")
    first_line = lines[0]
    level = len(first_line) - len(first_line.lstrip("#"))
    text = first_line.lstrip("#").strip()
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code_node = ParentNode("code", [child])
    return ParentNode("pre", [code_node])


def quote_to_html_node(block):
    lines = block.split("\n")
    text = "\n".join(line[1:].strip() for line in lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)


def ulist_to_html_node(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        text = line[2:].strip()
        text_children = text_to_children(text)
        children.append(ParentNode("li", text_children))
    return ParentNode("ul", children)


def olist_to_html_node(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        text = line[line.find(". ") + 2 :].strip()
        text_children = text_to_children(text)
        children.append(ParentNode("li", text_children))
    return ParentNode("ol", children)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    raise ValueError("invalid block type")
