from pathlib import Path
from block import markdown_to_html_node, markdown_to_blocks, block_to_block_type, block_to_html, BlockType
from htmlnode import ParentNode, LeafNode, HTMLNode
import os


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING:
            node = block_to_html(block, BlockType.HEADING)
            if node.tag == "h1":
                title = block.lstrip("# ").rstrip(" ")
                return title
        continue

    raise Exception ("no header found")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page {from_path} to {dest_path} using {template_path}")
    path = Path(from_path)
    template_path = Path(template_path)
    destination = Path(dest_path)

    contents = path.read_text(encoding="utf-8")
    template = template_path.read_text(encoding="utf-8")

    htmlnode = markdown_to_html_node(contents)
    html = htmlnode.to_html()
    title = extract_title(contents)

    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(full_html, encoding="utf-8")




def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    # 1. Loop through everything in the content folder
    for filename in os.listdir(dir_path_content):
        # 2. Create the full paths
        from_path = os.path.join(dir_path_content, filename)
        
        # 3. If it's a file, generate the page
        if os.path.isfile(from_path):
            # IMPORTANT: We want the destination to match the filename, but with .html
            dest_filename = filename.replace(".md", ".html")
            dest_path = os.path.join(dest_dir_path, dest_filename)
            generate_page(from_path, template_path, dest_path, basepath)
            
        # 4. If it's a directory, recurse into it
        elif os.path.isdir(from_path):
            new_dest_dir = os.path.join(dest_dir_path, filename)
            generate_pages_recursive(from_path, template_path, new_dest_dir, basepath)



