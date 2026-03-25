import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from markdown_blocks import markdown_to_html_node


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_lines(self):
        md = "\n\n\nFirst block\n\n\nSecond block\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])

    def test_single_block(self):
        md = "Just a single paragraph with **bold**"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just a single paragraph with **bold**"])

    def test_list_only(self):
        md = "- item 1\n- item 2\n- item 3"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["- item 1\n- item 2\n- item 3"])

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = "```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


class TestBlockToBlockType(unittest.TestCase):

    def test_headings(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        # 7 # is not valid
        self.assertEqual(
            block_to_block_type("####### Not a heading"), BlockType.PARAGRAPH
        )

    def test_code_block(self):
        code_block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(code_block), BlockType.CODE)
        short_code = "```\n```"
        self.assertEqual(block_to_block_type(short_code), BlockType.PARAGRAPH)
        single_line = "```some code```"
        self.assertEqual(block_to_block_type(single_line), BlockType.PARAGRAPH)

    def test_quote_block(self):
        quote = "> This is a quote\n> Another line"
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)
        quote_no_space = ">Quote line\n>Second line"
        self.assertEqual(block_to_block_type(quote_no_space), BlockType.QUOTE)
        mixed = "> Quote\nNormal line"
        self.assertEqual(block_to_block_type(mixed), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        ul = "- item 1\n- item 2\n- item 3"
        self.assertEqual(block_to_block_type(ul), BlockType.ULIST)
        bad_ul = "- item 1\n* item 2"
        self.assertEqual(block_to_block_type(bad_ul), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        ol = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(ol), BlockType.OLIST)
        ol_wrong = "1. first\n3. second\n4. third"
        self.assertEqual(block_to_block_type(ol_wrong), BlockType.PARAGRAPH)
        ol_start_2 = "2. second\n3. third"
        self.assertEqual(block_to_block_type(ol_start_2), BlockType.PARAGRAPH)

    def test_paragraph(self):
        text = "This is a normal paragraph of text."
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
