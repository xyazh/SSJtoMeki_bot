__version__ = "1.0.0"


if __name__ == "__main__":
    from mods.RollLibMod.roll.Dice import Roll
    r = Roll()
    print(r.dComplex(1+1j,1+3j))