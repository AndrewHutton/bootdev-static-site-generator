import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
   def test_eq(self):
      node = TextNode("This is a text node", TextType.BOLD)
      node2 = TextNode("This is a text node", TextType.BOLD)
      self.assertEqual(node, node2)

   def test_neq(self):
      node = TextNode("This is a text node", TextType.BOLD)
      node2 = TextNode("This is a text node", TextType.ITALIC)
      self.assertNotEqual(node, node2)

   def test_neq_url(self):
      node = TextNode("This is a text node", TextType.LINK, url="https://example.com")
      node2 = TextNode("This is a text node", TextType.LINK, url="https://example.org")
      self.assertNotEqual(node, node2)

   def test_url_none(self):
      node = TextNode("This is a text node", TextType.LINK)
      node2 = TextNode("This is a text node", TextType.LINK, url=None)
      self.assertEqual(node, node2)

   def test_neq_string(self):
      node = TextNode("This is a text node", TextType.TEXT)
      node2 = TextNode("This is a text node2", TextType.TEXT)
      self.assertNotEqual(node, node2)

   def test_repr(self):
      node = TextNode("This is a text node", TextType.BOLD)
      self.assertEqual(repr(node), "TextNode(This is a text node, bold,None)")


## FUNCTION TESTS
class TestTextNodeToHTMLNode(unittest.TestCase):
   def test_text(self):
      node = TextNode("This is a text node", TextType.TEXT)
      html_node = text_node_to_html_node(node)
      self.assertEqual(html_node.tag, None)
      self.assertEqual(html_node.value, "This is a text node")
      self.assertEqual(html_node.props, None)

   def test_text_image(self):
      node = TextNode("Example image", TextType.IMAGE, url="https://example.com/image.png")
      html_node = text_node_to_html_node(node)
      self.assertEqual(html_node.tag, "img")
      self.assertEqual(html_node.value, None)
      self.assertEqual(html_node.props, {"src": "https://example.com/image.png", "alt": "Example image"})

   def test_text_link(self):
      node = TextNode("Example", TextType.LINK, url="https://example.com")
      html_node = text_node_to_html_node(node)
      self.assertEqual(html_node.tag, "a")
      self.assertEqual(html_node.value, "Example")
      self.assertEqual(html_node.props, {"href": "https://example.com"})

   def test_text_link_no_url(self):
      node = TextNode("Example", TextType.LINK)
      html_node = text_node_to_html_node(node)
      self.assertEqual(html_node.tag, "a")
      self.assertEqual(html_node.value, "Example")
      self.assertEqual(html_node.props, {"href": None})

if __name__ == "__main__":
   unittest.main()