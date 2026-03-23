from textnode import TextNode, TextType


def main():
    node = TextNode(
        text="this is some anchor text",
        text_type=TextType.LINK,
        url="https://www.boot.dev",
    )
    print(node)


if __name__ == "__main__":
    main()
