def markdown_to_blocks(markdown: str) -> list[str]:
    raw_blocks = markdown.split("\n\n")

    blocks = []
    for block in raw_blocks:
        if block == "":
            continue
        stripped_block = block.strip()
        blocks.append(stripped_block)

    return blocks
