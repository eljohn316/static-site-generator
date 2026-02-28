import re
from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if node.text.count(delimiter) % 2 != 0 or delimiter not in ["`", "**", "_"]:
            raise TypeError("Invalid markdown syntax")

        new_nodes_parts = []

        delimiter_filter = re.escape(delimiter)
        pattern = f"{delimiter_filter}(.*?){delimiter_filter}"
        delimited_words = re.findall(pattern, node.text)

        for text in node.text.split(delimiter):
            if text == "":
                continue
            if text in delimited_words:
                new_nodes_parts.append(TextNode(text, text_type))
            else:
                new_nodes_parts.append(TextNode(text, TextType.TEXT))

        new_nodes.extend(new_nodes_parts)

    return new_nodes
