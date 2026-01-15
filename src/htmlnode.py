class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError ("not implemented")

    def props_to_html(self):
        if not self.props: # This handles both None and {}
            return ""
        
        attributes = []
        for key, value in self.props.items():
            attributes.append(f'{key}="{value}"')
        
        return " " + " ".join(attributes)
    def __repr__(self):
        return f"tags:{self.tag}, value:{self.value}, children:{self.children}, props:{self.props}"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("node must have a value")
        
        # If there is no tag, just return the raw text
        if not self.tag:
            return self.value
            
        # Otherwise, wrap it in tags
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tags are needed")
        if self.children is None:
            raise ValueError("children are needed")

        childrenhtml = ""
        for child in self.children:
            childrenhtml += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{childrenhtml}</{self.tag}>"

    

    