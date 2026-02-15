__version__ = "1.0.0"


if __name__ == "__main__":
    from roll.Dice import Dice
    r = Dice()
    print(r.dFloat(10,2).avg())