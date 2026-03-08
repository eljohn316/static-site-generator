import re
from enum import Enum


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
