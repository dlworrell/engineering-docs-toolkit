from xml.sax.saxutils import escape


def mi(name: str) -> str:
    return f"<mi>{escape(name)}</mi>"


def mn(value: str | int | float) -> str:
    return f"<mn>{escape(str(value))}</mn>"


def mo(operator: str) -> str:
    return f"<mo>{escape(operator)}</mo>"


def mrow(*items: str) -> str:
    return "<mrow>" + "".join(items) + "</mrow>"


def mathml(*items: str) -> str:
    return '<math xmlns="http://www.w3.org/1998/Math/MathML">' + "".join(items) + "</math>"
