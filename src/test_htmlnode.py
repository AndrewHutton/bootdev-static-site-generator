import unittest

from htmlnode import HTMLNode, LeafNode


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


if __name__ == "__main__":
   unittest.main()