from textnode import TextNode, TextType

# create a main function and call it
def main():
   node = TextNode("Here's some text", TextType.LINK, "https://example.com")
   print(node)




if __name__ == "__main__":
    main()