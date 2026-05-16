import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


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


   def test_split_image(self):
      node = TextNode(
         "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
         TextType.TEXT,
      )
      new_nodes = split_nodes_image([node])
      self.assertListEqual(
         [
               TextNode("This is text with an ", TextType.TEXT),
               TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
         ],
         new_nodes,
      )

   def test_split_image_single(self):
      node = TextNode(
         "![image](https://www.example.COM/IMAGE.PNG)",
         TextType.TEXT,
      )
      new_nodes = split_nodes_image([node])
      self.assertListEqual(
         [
               TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
         ],
         new_nodes,
      )

   def test_split_images(self):
      node = TextNode(
         "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
         TextType.TEXT,
      )
      new_nodes = split_nodes_image([node])
      self.assertListEqual(
         [
               TextNode("This is text with an ", TextType.TEXT),
               TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
               TextNode(" and another ", TextType.TEXT),
               TextNode(
                  "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
               ),
         ],
         new_nodes,
      )

   def test_split_links(self):
      node = TextNode(
         "This is text with a [link](https://boot.dev) and [another link](https://wikipedia.org) with text that follows",
         TextType.TEXT,
      )
      new_nodes = split_nodes_link([node])
      self.assertListEqual(
         [
               TextNode("This is text with a ", TextType.TEXT),
               TextNode("link", TextType.LINK, "https://boot.dev"),
               TextNode(" and ", TextType.TEXT),
               TextNode("another link", TextType.LINK, "https://wikipedia.org"),
               TextNode(" with text that follows", TextType.TEXT),
         ],
         new_nodes,
      )

class TestTextToTextNodes(unittest.TestCase):
   def test_text_to_textnodes(self):
      text = "This is **bold** text and this is _italic_ text."
      new_nodes = text_to_textnodes(text)
      expected_nodes = [
         TextNode("This is ", TextType.TEXT),
         TextNode("bold", TextType.BOLD),
         TextNode(" text and this is ", TextType.TEXT),
         TextNode("italic", TextType.ITALIC),
         TextNode(" text.", TextType.TEXT)
      ]
      self.assertEqual(new_nodes, expected_nodes)


if __name__ == "__main__":
   unittest.main()