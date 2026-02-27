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
            props.append(f"{key}={value}")

        return f" {" ".join(props)}"

    def __repr__(self):
        tag = self.tag or "''"
        value = self.value or "''"
        children = self.children or "''"
        props = self.props_to_html() if self.props else ""
        return f"HTMLNode({tag}, {value}, {children}, '{props}')"
