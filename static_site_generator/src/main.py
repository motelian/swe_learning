import os
from copystatic import recursive_copy
from gencontent import generate_pages_recursive
import sys

dir_path_static = "./static"
dir_path_public = "../docs"
dir_path_content = "./content"
template_path = "./template.html"

def main():

    basepath = "/"
    print(len(sys.argv))
    print(sys.argv[0])
    print(sys.argv[1])
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
        print(basepath)


    print("Copying static files to public directory...")
    recursive_copy(dir_path_static, dir_path_public)

    print("Generating pages...")
    generate_pages_recursive(
        dir_path_content,
        template_path,
        dir_path_public,
        basepath
    )

if __name__ == "__main__":
    main()
