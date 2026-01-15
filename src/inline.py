import re
from textnode import TextNode, TextType, split_nodes_delimiter

def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    # Same as images, but without the starting !
    pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)

def split_node_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        images = extract_markdown_images(text)

        if not images:
            new_nodes.append(node)
            continue
        
        for alt_text, url in images:
            image_markdown = f"![{alt_text}]({url})"
            sections = text.split(image_markdown, 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            text = sections[1]

        if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def split_node_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        links = extract_markdown_links(text)

        for texts, url in links:
            link_markdown = f"[{texts}]({url})"
            sections = text.split(link_markdown, 1)

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(texts, TextType.LINK, url))
            text = sections[1]
    
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    node = [TextNode(text, TextType.TEXT)]
    node = split_nodes_delimiter(node, "`", TextType.CODE)
    node = split_nodes_delimiter(node, "**", TextType.BOLD)
    node = split_nodes_delimiter(node, "_", TextType.ITALIC)
    node = split_node_links(node)
    node = split_node_images(node)
    return node





        
        

            
            

