def calculate(expression: str) -> float:
    """
    安全地计算数学表达式
    参数:
        expression: 数学表达式字符串，如 "(3+5)*2^3"
    返回:
        计算结果（浮点数或整数）
    异常:
        ValueError: 包含非法字符或表达式无效
        ZeroDivisionError: 除零错误
    """
    allowed_chars = set("0123456789+-*/().%^ ")
    expression = expression.replace("x", "*").replace("÷", "/")
    if not all(c in allowed_chars for c in expression):
        raise ValueError(
            "表达式中包含非法字符，仅允许数字、运算符、括号、小数点和百分号"
        )

    # 将 ^ 替换为 Python 幂运算符 **
    expression = expression.replace("^", "**")

    try:
        result = eval(expression)
        return result
    except ZeroDivisionError:
        raise ZeroDivisionError("数学错误：不能除以零")
    except SyntaxError:
        raise ValueError("表达式语法无效")
    except Exception as e:
        raise ValueError(f"表达式计算失败: {e}")


# 使用示例
if __name__ == "__main__":
    # 从函数入口直接传入表达式获得结果
    try:
        res = calculate("(123 + 456) x 789 / 12")
        print(res)  # 输出 64.0
    except Exception as e:
        print(e)
