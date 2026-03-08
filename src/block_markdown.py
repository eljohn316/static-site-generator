import re

from enum import Enum
from htmlnode import ParentNode
from textnode import TextNode, text_node_to_html_node, TextType
from extract_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    raw_blocks = markdown.split("\n\n")

    blocks = []
    for block in raw_blocks:
        if block == "":
            continue
        stripped_block = block.strip()
        blocks.append(stripped_block)

    return blocks


def validate_ordered_list(text: str) -> bool:
    pattern = r"^(\d+)\.\s(.*)"

    matches = []
    for line in text.split("\n"):
        match_found = re.match(pattern, line)
        if match_found:
            matches.append((int(match_found.group(1)), match_found.group(2)))

    if not matches:
        return False

    expected_number = 1
    for i, (actual_number, text) in enumerate(matches):
        if actual_number != expected_number:
            return False
        expected_number += 1

    return True


def block_to_block_type(md_text: str) -> BlockType:
    # Matching for Headings
    if re.match(r"^(#{1,6})\s+(.+)$", md_text):
        return BlockType.HEADING

    # Matching for Code blocks
    elif re.match(r"^```(\w+)?\s*\n([\s\S]*?)\n```$", md_text):
        return BlockType.CODE

    # Matching for Quotes
    elif re.match(r"^>\s?.+", md_text):
        return BlockType.QUOTE

    # Matching for Unordered list
    elif re.match(r"^-\s.*", md_text):
        return BlockType.ULIST

    # Matching for Ordered list
    elif validate_ordered_list(md_text):
        return BlockType.OLIST

    # Defaults to paragraph
    else:
        return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        parts = item.split(". ", 1)
        text = parts[1]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def extract_title(markdown: str) -> str:
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        if block.startswith("# "):
            block = block.strip("#").strip()
            return block

    raise Exception("No 'h1' header found")
