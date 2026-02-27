import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello World")
        self.assertEqual(node.to_html(), "<p>Hello World</p>")

    def test_leaf_empty_to_html(self):
        node = LeafNode(None, "Hello World")
        self.assertEqual(node.to_html(), "Hello World")

    def test_left_props_to_html(self):
        node = LeafNode("a", "See source", {"href": "boot.dev", "class": "link"})
        self.assertEqual(
            node.to_html(), '<a href="boot.dev" class="link">See source</a>'
        )


if __name__ == "__main__":
    unittest.main()
