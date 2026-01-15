#print("hello world")
from textnode import TextNode, TextType
from copystatic import copy_files_recursive
import os
import shutil
from page_generator import generate_page, generate_pages_recursive
import sys

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    # Create a TextNode with dummy data
    #node = TextNode("some text here", TextType.LINK, "https://example.com")
    
    # Print it
    #print(node)

    dir_path_static = "./static"
    dir_path_docs = "./docs" 
    dir_path_content = "./content"
    template_path = "./template.html"

    copy_files_recursive(dir_path_static, dir_path_docs)
    #generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive(dir_path_content, template_path, dir_path_docs, basepath)

# Actually call the function
main()
