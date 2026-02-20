__version__ = "1.0.0"


if __name__ == "__main__":
    from roll.Roll import Roll
    r = Roll()
    ra = r.ra("力量",1, 2, True)
    print(ra.bonus())
    print(ra.punishment())
    print(ra.toStr())


