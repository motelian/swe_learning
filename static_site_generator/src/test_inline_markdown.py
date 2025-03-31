import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType

class InlineMarkdownTest(unittest.TestCase):
    def test_code(self):
        nodes = [TextNode("This is text with a `code block` word", TextType.TEXT)]
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), expected)

    def test_multi_text_type_nodes(self):
        nodes = [
            TextNode("def add(a,b):\n return a+b", TextType.CODE),
            TextNode("This is text with a **bold text** word", TextType.TEXT)
        ]
        expected = [
            TextNode("def add(a,b):\n return a+b", TextType.CODE),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "**", TextType.BOLD), expected)

        def test_delim_bold_double(self):
            node = TextNode(
                "This is text with a **bolded** word and **another**", TextType.TEXT
            )
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
            self.assertListEqual(
                [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("bolded", TextType.BOLD),
                    TextNode(" word and ", TextType.TEXT),
                    TextNode("another", TextType.BOLD),
                ],
                new_nodes,
            )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_empty_string(self):
        nodes = [
            TextNode("This is **** text with a **bold text** word", TextType.TEXT)
        ]
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode(" text with a ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "**", TextType.BOLD), expected)

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual(
            extract_markdown_images(text),
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )
