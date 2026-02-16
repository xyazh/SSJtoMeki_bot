__version__ = "1.0.0"


if __name__ == "__main__":
    from roll.tools.Expression import Expression
    print(Expression("1+100*j/2").eval())