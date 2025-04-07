from argparse import PARSER
from textnode import TextType, TextNode, text_node_to_html_node
from inline_markdown import (
    text_to_textnodes
)
from htmlnode import ParentNode, LeafNode
from enum import Enum
import re

# create a new BlockType enum with block types below:
# paragraph, heading, etc
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    ORDERED_LIST = "ordered_list"
    UNORDERED_LIST = "unordered_list"
    QUOTE = "quote"
    CODE = "code"


def markdown_to_html_node(markdown):
    # converts a full markdown document into a single parent HTMLNode

    # split the markdown into blocks
    blocks = markdown_to_blocks(markdown)
    html_body_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            lines = block.split("\n")
            paragraph = " ".join(lines)
            children = text_to_children(paragraph)
            html_body_nodes.append(ParentNode("p", children))

        if block_type == BlockType.HEADING:
            match_pattern = re.match(r"(^#{1,7})(.*)", block)
            md_syntax = match_pattern.group(1)
            raw_text = match_pattern.group(2).strip()
            children = text_to_children(raw_text)
            html_body_nodes.append(ParentNode(f"h{len(md_syntax)}", children))

        if block_type == BlockType.QUOTE:
            raw_text = " ".join(map(lambda x: x[1:].strip(), block.split("\n")))
            children = text_to_children(raw_text)
            html_body_nodes.append(ParentNode("blockquote", children))

        if block_type == BlockType.ORDERED_LIST:
            block_nodes = []
            for line in block.split("\n"):
                line_text = line[2:].strip()
                item_children = text_to_children(line_text)
                block_nodes.append(ParentNode("li", item_children))
            html_body_nodes.append(ParentNode("ol", block_nodes))

        if block_type == BlockType.UNORDERED_LIST:
            block_nodes = []
            for line in block.split("\n"):
                line_text = line[1:].strip()
                item_children = text_to_children(line_text)
                block_nodes.append(ParentNode("li", item_children))
            html_body_nodes.append(ParentNode("ul", block_nodes))

        if block_type == BlockType.CODE:
            code = block.split("```")[1]
            html_body_nodes.append(
                ParentNode("pre", [text_node_to_html_node(TextNode(code, TextType.CODE))])
            )
    return ParentNode("div", html_body_nodes)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("#"):
            return line[1:].strip()
    raise Exception("title not found")

def text_to_children(text):
    textnodes = text_to_textnodes(text)
    return list(map(text_node_to_html_node, textnodes))


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return list(filter(None, map(lambda x:x.strip(), blocks)))

def block_to_block_type(block):

    def is_match(pattern):
        def inner(line):
            return bool(re.search(pattern, line))
        return inner

    lines = block.split("\n")

    pattern_blocktype = {
        BlockType.HEADING: r"^#{1,7} ",
        BlockType.QUOTE: r"^>",
        BlockType.UNORDERED_LIST: r"^- "
    }

    # check if the block is one of headings, quote, unordered list types
    for k, v in pattern_blocktype.items():
        if all(map(is_match(v), lines)):
            return k

    # check if the block is a code
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # check if the block is an ordered list
    is_ordered_list = 1
    for i, l in enumerate(lines):
        if not l.startswith(f"{i+1}. "):
            is_ordered_list = 0
            break
    if is_ordered_list == 1:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
