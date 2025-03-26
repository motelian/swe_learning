from textnode import *

def main():
    text = "this is a caption for an image"
    text_type = TextType.IMAGE
    url = "https://example.com/image.jpg"
    example = TextNode(text, text_type, url)
    print(example)

if __name__ == "__main__":
    main()
