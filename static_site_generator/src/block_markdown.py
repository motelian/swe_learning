from textnode import TextType, TextNode
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


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return list(filter(None, map(lambda x:x.strip(), blocks)))

def markdown_to_html_node(markdown):
    # converts a full markdown document into a single parent HTMLNode
    pass

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

    for k, v in pattern_blocktype.items():
        if all(map(is_match(v), lines)):
            return k

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    is_ordered_list = 1
    for i, l in enumerate(lines):
        if not l.startswith(f"{i+1}. "):
            is_ordered_list = 0
            break

    if is_ordered_list == 1:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
