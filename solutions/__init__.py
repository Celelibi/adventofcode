import importlib

for i in range(1, 26):
    try:
        name = "solutions.day%02d" % i
        importlib.import_module(name)
    except ModuleNotFoundError as e:
        if e.name != name:
            raise
