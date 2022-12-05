import importlib
import os

solutions_path = os.path.dirname(os.path.relpath(__file__))

for e in os.listdir(os.path.join(solutions_path, "..", "solutions")):
    try:
        year = int(e)
    except ValueError:
        continue

    if year < 2015:
        continue

    for i in range(1, 26):
        name = "solutions.%d.day%02d" % (year, i)
        try:
            importlib.import_module(name)
        except ModuleNotFoundError as e:
            if e.name != name:
                raise
