from typing import Union


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if not self.props:
            return ""

        props = []
        for key, value in self.props.items():
            props.append(f'{key}="{value}"')

        return f" {" ".join(props)}"

    def __repr__(self):
        tag = self.tag or "''"
        value = self.value or "''"
        children = self.children or "''"
        props = self.props_to_html() if self.props else ""
        return f"HTMLNode({tag}, {value}, {children}, '{props}')"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf node must have a value")

        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        tag = self.tag or "''"
        value = self.value or "''"
        props = self.props_to_html() if self.props else ""
        return f"HTMLNode({tag}, {value}, '{props}')"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list[Union["ParentNode", "LeafNode"]],
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent node must have a tag")

        if self.children is None:
            raise ValueError("Children is required")

        children = ""
        for node in self.children:
            children += node.to_html()

        return f"<{self.tag}>{children}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
