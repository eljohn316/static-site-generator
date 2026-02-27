import unittest


from src.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_htmlnode_repr(self):
        node = HTMLNode(
            "a",
            "See source",
            [HTMLNode("span", "Deprecated soon")],
            {"class": "link", "href": "https://www.boot.dev"},
        )
        self.assertEqual(
            repr(node),
            "HTMLNode(a, See source, [HTMLNode(span, Deprecated soon, '', '')], ' class=link href=https://www.boot.dev')",
        )

    def test_empty_htmlnode_repr(self):
        node = HTMLNode()
        self.assertEqual(
            repr(node),
            "HTMLNode('', '', '', '')",
        )

    def test_htmlnode_props(self):
        node = HTMLNode(
            "a",
            "See source",
            [HTMLNode("span", "Deprecated soon")],
            {"class": "link", "href": "https://www.boot.dev"},
        )
        self.assertEqual(node.props_to_html(), " class=link href=https://www.boot.dev")

    def test_htmlnode_empty_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
