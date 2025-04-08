import os
from block_markdown import markdown_to_html_node, extract_title

def generate_pages_recursive(content_dir_path, template_path, dest_dir_path):
    if not os.path.exists(content_dir_path):
        raise Exception("Content directory not found")

    for filename in os.listdir(content_dir_path):
        from_path = os.path.join(content_dir_path, filename)
        if os.path.isfile(from_path):
            if filename[-2:] == "md":
                dest_filename = filename[:-2] + "html"
                dest_path = os.path.join(dest_dir_path, dest_filename)
                generate_page(from_path, template_path, dest_path)
            else:
                continue
        else:
            dest_path = os.path.join(dest_dir_path, filename)
            generate_pages_recursive(from_path, template_path, dest_path)

def generate_page(from_path, template_path, dest_path):
    if not os.path.exists(from_path):
        raise FileNotFoundError(f"file {from_path} does not exist")
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"file {template_path} does not exist")


    print(f" * {from_path} {template_path} -> {dest_path}")

    with open(from_path, "r") as f:
        md = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(page)
