from markdown_blocks import markdown_to_html_node
import os
from pathlib import Path


def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("no h1 header found")


def generate_page(from_path, template_path, dest_path, basepath):
    print(
        f"Generating page from {from_path} using template {template_path} to {dest_path}"
    )
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    html_page = template.replace("{{ Title }}", title)
    html_page = html_page.replace("{{ Content }}", html_string)
    html_page = html_page.replace('href="/', f'href="{basepath}')
    html_page = html_page.replace('src="/', f'src="{basepath}')
    directory = os.path.dirname(dest_path)
    os.makedirs(directory, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(html_page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for entry in os.scandir(dir_path_content):
        if entry.is_file() and entry.name.endswith(".md"):
            from_path = entry.path
            dest_path = os.path.join(dest_dir_path, entry.name[:-3] + ".html")
            generate_page(from_path, template_path, dest_path, basepath)
        elif entry.is_dir():
            new_dest_dir_path = os.path.join(dest_dir_path, entry.name)
            generate_pages_recursive(
                entry.path, template_path, new_dest_dir_path, basepath
            )
