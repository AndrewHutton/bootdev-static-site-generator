
class HTMLNode:
   def __init__(self, tag = None, value = None, children = None, props = None):
      self.tag = tag
      self.value = value
      self.children = children
      self.props = props

   def to_html(self):
      raise NotImplementedError("to_html method must be implemented by subclasses")
   
   def props_to_html(self):
      string = ""
      if self.props:
         for key, value in self.props.items():
            string += f' {key}="{value}"'
         return string
      
      return string
   

   def __repr__(self):
      return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
      


class LeafNode(HTMLNode):
   def __init__(self, tag = None, value = None, props = None):
      super().__init__(tag=tag, value=value, children=None, props=props)

   def to_html(self):
      if not self.value:
         raise ValueError("LeafNode must have a value to convert to HTML")
      
      if not self.tag:
         return self.value
      else:
         return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
      
   def __repr__(self):
      return f"LeafNode({self.tag}, {self.value}, {self.props})"
   


class ParentNode(HTMLNode):
   def __init__(self, tag, children, props = None):
      super().__init__(tag=tag, value=None, children=children, props=props)

   def to_html(self):
      if not self.tag:
         raise ValueError("ParentNode must have a tag to convert to HTML")
      if not self.children:
         raise ValueError("ParentNode must have children to convert to HTML")
      
      return_string = ""
      for child in self.children:
         return_string += child.to_html()
      return f"<{self.tag}{self.props_to_html()}>{return_string}</{self.tag}>"
   
   
      
      