#print("hello world")
from textnode import TextNode, TextType
from copystatic import copy_files_recursive
import os
import shutil
from page_generator import generate_page, generate_pages_recursive

def main():
    # Create a TextNode with dummy data
    node = TextNode("some text here", TextType.LINK, "https://example.com")
    
    # Print it
    print(node)

    copy_files_recursive("./static", "./public")
    #generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "public")

# Actually call the function
main()
