import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links


class TestInlineMarkdown(unittest.TestCase):
   def test_delim_bold(self):
      node = TextNode("This is **bold** text", TextType.TEXT)
      new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
      expected_nodes = [
         TextNode("This is ", TextType.TEXT),
         TextNode("bold", TextType.BOLD),
         TextNode(" text", TextType.TEXT)
      ]
      self.assertEqual(new_nodes, expected_nodes)

   def test_split_nodes_delimiter_unclosed(self):
      nodes = [TextNode("This is **bold text", TextType.TEXT)]
      with self.assertRaises(ValueError):
         split_nodes_delimiter(nodes, "**", TextType.BOLD)

   def test_split_nodes_delimiter_multiple(self):
      nodes = [TextNode("This is **bold** and **another bold** text", TextType.TEXT)]
      new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
      expected_nodes = [
         TextNode("This is ", TextType.TEXT),
         TextNode("bold", TextType.BOLD),
         TextNode(" and ", TextType.TEXT),
         TextNode("another bold", TextType.BOLD),
         TextNode(" text", TextType.TEXT)
      ]
      self.assertEqual(new_nodes, expected_nodes)      

   def test_delim_italic(self):
      node = TextNode("This is _italic_ text", TextType.TEXT)
      new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
      expected_nodes = [
         TextNode("This is ", TextType.TEXT),
         TextNode("italic", TextType.ITALIC),
         TextNode(" text", TextType.TEXT)
      ]
      self.assertEqual(new_nodes, expected_nodes)  

   def test_delim_bold_and_italic(self):
      node = TextNode("This is **bold** and _italic_ text", TextType.TEXT)
      new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
      new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
      expected_nodes = [
         TextNode("This is ", TextType.TEXT),
         TextNode("bold", TextType.BOLD),
         TextNode(" and ", TextType.TEXT),
         TextNode("italic", TextType.ITALIC),
         TextNode(" text", TextType.TEXT)
      ]
      self.assertEqual(new_nodes, expected_nodes)

   def test_delim_multi_nodes(self):
      nodes = [
         TextNode("This is **bold** text", TextType.TEXT),
         TextNode("This is _italic_ text", TextType.TEXT)
      ]
      new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
      new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
      expected_nodes = [
         TextNode("This is ", TextType.TEXT),
         TextNode("bold", TextType.BOLD),
         TextNode(" text", TextType.TEXT),
         TextNode("This is ", TextType.TEXT),
         TextNode("italic", TextType.ITALIC),
         TextNode(" text", TextType.TEXT)
      ]
      self.assertEqual(new_nodes, expected_nodes)


   def test_extract_markdown_images(self):
      matches = extract_markdown_images(
         "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
      )
      self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

   def test_extract_markdown_links(self):
      matches = extract_markdown_links(
         "This is text with a [link to google](https://www.google.com)"
      )
      self.assertListEqual([("link to google", "https://www.google.com")], matches)


   def test_extract_markdown_links_and_images(self):
      text = "This is text with a [link to google](https://www.google.com) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
      matches = []
      link_matches = extract_markdown_links(text)
      image_matches = extract_markdown_images(text)
      matches.extend(link_matches)
      matches.extend(image_matches)
      self.assertListEqual([
         ('link to google', 'https://www.google.com'),
         ('image', 'https://i.imgur.com/zjjcJKZ.png')
      ], matches)

if __name__ == "__main__":
   unittest.main()