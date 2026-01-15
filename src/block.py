from enum import Enum
from textnode import TextNode, text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragragh"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_block_type(block):
    lines = block.splitlines()

    # Heading: 1-6 hashes followed by a space
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    # Code: Starts and ends with 3 backticks
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # Quote: Every line must start with >
    if block.startswith(">"):
        if all(line.startswith(">") for line in lines):
            return BlockType.QUOTE

    # Unordered List: Every line must start with - or *
    if block.startswith(("- ", "* ")):
        if all(line.startswith(("- ", "* ")) for line in lines):
            return BlockType.UNORDERED_LIST

    # Ordered List: Checks for 1. 2. 3. sequence
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
    

def markdown_to_blocks(markdown):
    # Split the document by double newlines
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    
    for block in blocks:
        # Remove leading/trailing whitespace
        stripped_block = block.strip()
        
        # Only add the block if it's not an empty string
        if stripped_block != "":
            filtered_blocks.append(stripped_block)
            
    return filtered_blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    child_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block_htmlnode = block_to_html(block, block_type)
        child_nodes.append(block_htmlnode)
    root_div = ParentNode(tag = "div", children = child_nodes)
    return root_div

def text_to_children(text):
    text_nodes = text_to_textnodes(text)     # you already wrote this
    children = []
    for node in text_nodes:
        child = text_node_to_html_node(node)   # you already wrote this too
        children.append(child)
    return children

def block_to_html(block, type):
    if type.value == "paragraph":
        lines = block.splitlines()
        joined = " ".join(lines)
        children = text_to_children(joined)
        return ParentNode(tag = "p", children = children)
    elif type.value == "heading":
        count = 0
        for char in block:
            if char == '#':
                count += 1
            else:
                break
        head = block.lstrip("#").lstrip(" ")
        children = text_to_children(head)
        return ParentNode(tag = f"h{count}", children = children)
    elif type.value == "code":
        # 1. Remove the backticks by slicing
        content = block[3:-3]
        
        # 2. Use .strip() to remove the leading and trailing newlines 
        # that Markdown often leaves inside the triple backticks
        content = content.strip("\n")
        
        # 3. Add exactly ONE newline at the end to satisfy the test's 
        # requirement for the closing tag: \n</code>
        content = content + "\n"
        
        code_node = LeafNode("code", content)
        return ParentNode(tag="pre", children=[code_node])
    elif type.value == "quote":
        lines = block.splitlines()
        stripped = []
        for line in lines:
            stripped.append(line.lstrip(">").strip())
        joined = " ".join(stripped)
        children = text_to_children(joined)
        return ParentNode(tag = "blockquote", children = children)

    elif type.value == "unordered list":
        lines = block.splitlines()
        stripped = []
        li_nodes = []
        for line in lines:
            if line.startswith("* "):
                stripped.append(line.removeprefix("* "))
            else:
                if line.startswith("- "):
                    stripped.append(line.removeprefix("- "))
        for text in stripped:
            child = text_to_children(text)
            li_node = ParentNode(tag = "li", children = child)
            li_nodes.append(li_node)
        return ParentNode(tag = "ul", children = li_nodes)

    elif type.value == "ordered list":
        lines = block.splitlines()
        li_nodes = []
        for i, line in enumerate(lines):
            prefix = f"{i + 1}. "
            cleaned = line.removeprefix(prefix)
            children = text_to_children(cleaned)
            li_node = ParentNode(tag = "li", children = children)
            li_nodes.append(li_node)
        return ParentNode(tag = "ol", children = li_nodes)

    else:
        lines = block.splitlines()
        joined = " ".join(lines)
        children = text_to_children(joined)
        return ParentNode(tag = "p", children = children)
        

        






        
        
        
        





