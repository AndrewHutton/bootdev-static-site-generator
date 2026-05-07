import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
   def test_repr(self):
      node = HTMLNode(tag="p", value="This is a paragraph", children=[], props={})
      self.assertEqual(repr(node), "HTMLNode(p, This is a paragraph, [], {})")

   def test_neq(self):
      node = HTMLNode(tag="p", value="This is a paragraph", children=[], props={})
      node2 = HTMLNode(tag="p", value="This is a different paragraph", children=[], props={})
      self.assertNotEqual(node, node2)

   def test_props_to_html(self):
      node = HTMLNode(tag="p", value="This is a paragraph", children=[], props={"class": "text"})
      self.assertEqual(node.props_to_html(), ' class="text"')

   def test_props_to_html_multiple(self):
      node = HTMLNode(tag="p", value="This is a paragraph", children=[], props={"class": "text", "id": "para-1"})
      self.assertEqual(node.props_to_html(), ' class="text" id="para-1"')
                       
   def test_to_html_not_implemented(self):
      node = HTMLNode(tag="p", value="This is a paragraph", children=[], props={})
      with self.assertRaises(NotImplementedError):
         node.to_html()


class TestLeafNode(unittest.TestCase):
   def test_to_html_with_props(self):
      node = LeafNode(tag="p", value="This is a paragraph", props={"class": "text"})
      self.assertEqual(node.to_html(), '<p class="text">This is a paragraph</p>')

   def test_to_html_no_tag(self):
      node = LeafNode(tag=None, value="This is a paragraph", props=None)
      self.assertEqual(node.to_html(), "This is a paragraph")

   def test_to_html_no_value(self):
      node = LeafNode(tag="p", value=None, props={"class": "text"})
      with self.assertRaises(ValueError):
         node.to_html()

   def test_repr(self):
      node = LeafNode(tag="p", value="This is a paragraph", props={"class": "text"})
      self.assertEqual(repr(node), "LeafNode(p, This is a paragraph, {'class': 'text'})")

   def test_to_html_multiple_props(self):
      node = LeafNode(tag="div", value="This is a div", props={"class": "container", "id": "main"})
      self.assertEqual(node.to_html(), '<div class="container" id="main">This is a div</div>')


class TestParentNode(unittest.TestCase):
   def test_to_html_with_children(self):
    child_node = LeafNode("span", "child")
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

   def test_to_html_with_grandchildren(self):
      grandchild_node = LeafNode("b", "grandchild")
      child_node = ParentNode("span", [grandchild_node])
      parent_node = ParentNode("div", [child_node])
      self.assertEqual(
         parent_node.to_html(),
         "<div><span><b>grandchild</b></span></div>",
      )

   def test_to_html_no_tag(self):
      child_node = LeafNode("span", "child")
      parent_node = ParentNode(None, [child_node])
      with self.assertRaises(ValueError):
         parent_node.to_html()

   def test_to_html_nested_children(self):
      grandchild_node1 = LeafNode("b", "grandchild1")
      grandchild_node2 = LeafNode("i", "grandchild2")
      child_node = ParentNode("span", [grandchild_node1, grandchild_node2])
      parent_node = ParentNode("div", [child_node])
      self.assertEqual(
         parent_node.to_html(),
         "<div><span><b>grandchild1</b><i>grandchild2</i></span></div>",
      )

   def test_to_html_with_props(self):
      child_node = LeafNode("span", "child")
      parent_node = ParentNode("div", [child_node], props={"class": "container"})
      self.assertEqual(
         parent_node.to_html(),
         '<div class="container"><span>child</span></div>',
      )

   def test_to_html_no_children(self):
      parent_node = ParentNode("div", [])
      with self.assertRaises(ValueError):
         parent_node.to_html()

   def test_to_html_multiple_props(self):
      child_node = LeafNode("bold", "child")
      parent_node = ParentNode("div", [child_node], props={"class": "container", "id": "main"})
      self.assertEqual(
         parent_node.to_html(),
         '<div class="container" id="main"><bold>child</bold></div>',
      )


if __name__ == "__main__":
   unittest.main()