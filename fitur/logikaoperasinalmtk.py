import ast


OPERATORS = {"+", "-", "*", "/"}


def _safe_eval(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    if isinstance(node, ast.BinOp):
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            if right == 0:
                raise ZeroDivisionError
            return left / right
        raise ValueError("Operator tidak didukung")
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_safe_eval(node.operand)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    raise ValueError("Ekspresi tidak valid")


def _format_result(value: float) -> str:
    if value.is_integer():
        return str(int(value))
    return str(value)


def evaluate_expression(expression: str) -> str:
    tree = ast.parse(expression, mode="eval")
    return _format_result(_safe_eval(tree))


def process_input(current_expression: str, key: str) -> str:
    if key == "=":
        if not current_expression or current_expression[-1] in OPERATORS:
            return current_expression
        try:
            return evaluate_expression(current_expression)
        except (ValueError, ZeroDivisionError, SyntaxError):
            return "Error"

    if key.isdigit():
        if current_expression == "Error":
            return key
        return current_expression + key

    if key in OPERATORS:
        if current_expression == "Error":
            return ""
        if not current_expression:
            return "-" if key == "-" else ""
        if current_expression[-1] in OPERATORS:
            return current_expression[:-1] + key
        return current_expression + key

    return current_expression
