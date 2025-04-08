import os
from copystatic import recursive_copy
from gencontent import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():

    print("Copying static files to public directory...")
    recursive_copy(dir_path_static, dir_path_public)

    print("Generating pages...")
    generate_pages_recursive(
        dir_path_content,
        template_path,
        dir_path_public,
    )

if __name__ == "__main__":
    main()
