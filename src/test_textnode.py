import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
   unittest.main()