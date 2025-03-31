import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    def convert_to_textnode(split_text):
        text_node_list = []
        for i, text in enumerate(split_text):
            if text == '':
                continue
            elif i%2 == 0:
                type_of_text = TextType.TEXT
            else:
                type_of_text = text_type
            text_node_list.append(TextNode(text, type_of_text))
        return text_node_list

    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            sections = node.text.split(delimiter)
            if len(sections) % 2 == 0:
                raise ValueError("invalid markdown, formatted section not closed")
            text_node_list = convert_to_textnode(sections)
            new_nodes.extend(text_node_list)

    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)
