import os
import shutil


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


dir_path_static = "./static"
dir_path_public = "./public"


def main():
    copy_contents(dir_path_static, dir_path_public)


if __name__ == "__main__":
    main()
