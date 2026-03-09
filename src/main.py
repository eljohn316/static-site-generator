import os
import shutil
from pathlib import Path

from block_markdown import markdown_to_html_node, extract_title


dir_path_static = "./static"
dir_path_public = "./public"


def copy_contents(src: str, dest: str):
    src_dir = os.path.abspath(src)
    dest_dir = os.path.abspath(dest)

    if not os.path.exists(src_dir):
        raise Exception("Invalid source path")

    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    print(f"Path: '{src_dir}'")

    shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)

    src_contents = os.listdir(src_dir)

    for content in src_contents:
        curr_content = os.path.join(src_dir, content)
        if os.path.isfile(curr_content):
            shutil.copy(curr_content, dest_dir)
        else:
            new_dest_dir = os.path.join(dest_dir, content)
            os.mkdir(new_dest_dir)
            copy_contents(curr_content, new_dest_dir)


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(
        f"Generating page from '{from_path}' to '{dest_path}' using '{template_path}'"
    )

    with open(from_path) as f:
        markdown = f.read()

    with open(template_path) as f:
        template = f.read()

    html_str = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html_str)

    with open(dest_path, "w") as f:
        f.write(template)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
):
    contents = os.listdir(dir_path_content)
    for content in contents:
        curr_content = os.path.join(os.path.abspath(dir_path_content), content)
        if os.path.isfile(curr_content):
            generate_page(
                curr_content,
                template_path,
                dest_dir_path + "/" + f"{content.strip('.md')}.html",
            )
        else:
            new_dest_dir_path = Path(
                os.path.join(os.path.abspath(dest_dir_path), content)
            )
            new_dest_dir_path.mkdir(exist_ok=True)
            print(new_dest_dir_path.as_posix())
            generate_pages_recursive(
                curr_content, template_path, new_dest_dir_path.as_posix()
            )


def main():
    # copy_contents(dir_path_static, dir_path_public)
    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
