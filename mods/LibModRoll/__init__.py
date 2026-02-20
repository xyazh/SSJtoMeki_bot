__version__ = "1.0.0"


if __name__ == "__main__":
    from roll.Roll import Roll
    r = Roll()
    ra = r.ra(None, 100, 100000000000000000000000000000)
    print(ra.count(),sum(ra.count()))
