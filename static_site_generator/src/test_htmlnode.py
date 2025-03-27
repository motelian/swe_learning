from htmlnode import HTMLNode, LeafNode, ParentNode
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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )
