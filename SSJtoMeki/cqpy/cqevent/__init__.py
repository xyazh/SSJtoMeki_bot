import os
for i in os.listdir(__path__[0]):
    if "_" in i:
        continue
    __import__("cqpy.cqevent." + i[:-3])
