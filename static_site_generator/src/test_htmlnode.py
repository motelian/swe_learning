from htmlnode import HTMLNode
import unittest

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a", "link", None, {"href": "https://example.com"})
        node2 = HTMLNode("a", "link", None, {"href": "https://example.com"})
        self.assertEqual(node, node2)

    def test_values(self):
        node = HTMLNode("div", "I wish I could read")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "I wish I could read")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_prop_to_html(self):
        node = HTMLNode("a", "link", None, {"href": "https://example.com"})
        node2 = HTMLNode("a", "link", None, {"href": "https://example.com", "rel": "nofollow"})
        node3 = HTMLNode("a", "link", None, None)
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')
        self.assertEqual(node2.props_to_html(), ' href="https://example.com" rel="nofollow"')
        self.assertEqual(node3.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode("a", "link", [], {"href": "https://example.com"})
        node2 = HTMLNode("a", "link")
        self.assertEqual(repr(node), "HTMLNode(a, link, [], {'href': 'https://example.com'})")
        self.assertEqual(repr(node2), "HTMLNode(a, link, None, None)")
