from html import escape


def inline_mathml(latex: str) -> str:
    body = escape(latex)
    return f'<math xmlns="http://www.w3.org/1998/Math/MathML" alttext="{body}"><mtext>{body}</mtext></math>'


def display_mathml(latex: str) -> str:
    body = escape(latex)
    return f'<math xmlns="http://www.w3.org/1998/Math/MathML" display="block" alttext="{body}"><mtext>{body}</mtext></math>'
