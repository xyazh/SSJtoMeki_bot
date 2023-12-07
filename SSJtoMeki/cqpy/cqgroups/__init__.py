import os
for i in os.listdir(__path__[0]):
    item_path = os.path.join(__path__[0], i)
    if "_" in i:
        continue
    if not os.path.isfile(item_path):
        continue
    __import__("cqpy.cqgroups." + i[:-3])