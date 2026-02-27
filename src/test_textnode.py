import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node_1 = TextNode("This is a text node", TextType.BOLD)
        node_2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node_1, node_2)

    def test_not_eq(self):
        node_1 = TextNode("This is a plain text node", TextType.TEXT)
        node_2 = TextNode("This is a bold text node", TextType.BOLD)
        self.assertNotEqual(node_1, node_2)

    def test_url(self):
        node_1 = TextNode("Learn to code here", TextType.LINK, "https://www.boot.dev")
        node_2 = TextNode("Learn to code here", TextType.LINK)
        self.assertNotEqual(node_1, node_2)

    def test_eq_url(self):
        node_1 = TextNode("Learn to code here", TextType.LINK, "https://www.boot.dev")
        node_2 = TextNode("Learn to code here", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node_1, node_2)

    def test_not_eq_url(self):
        node_1 = TextNode("Here is the link", TextType.LINK, "https://www.facebook.com")
        node_2 = TextNode("Here is the link", TextType.LINK, "https://www.google.com")
        self.assertNotEqual(node_1, node_2)


if __name__ == "__main__":
    unittest.main()
