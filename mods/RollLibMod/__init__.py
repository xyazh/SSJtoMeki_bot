__version__ = "1.0.0"


if __name__ == "__main__":
    from roll.Dice import Dice
    r = Dice()
    print(r.d(10000000000000000000000000000000000,100000000000000000000000000000000))