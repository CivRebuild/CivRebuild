
import os
from pathlib import Path

build_dirs = [
    "Debug",
    "Release-symbols",
    "Release-light",
    "Release",
]

core_dir = os.path.abspath("../../../CoreEngine")
python_dirs = [
    Path(os.path.abspath("Python")),
    Path(os.path.abspath("../../../Assets/Python")),
]

new_pythonpath = []

#  add core dir
new_pythonpath.append(os.path.abspath(core_dir))

# add CvGameCoreDLL build dirs
dll_path = os.path.abspath("../CvGameCoreDLL")
for _dir in build_dirs:
    new_pythonpath.append(os.path.abspath(os.path.join(dll_path, "x64", "lin", _dir)))
    new_pythonpath.append(os.path.abspath(os.path.join(dll_path, "x64", "win", _dir)))

# add python dirs
for py_dir in python_dirs:
    new_pythonpath.append(str(py_dir.parents[0]))
    new_pythonpath.append(str(py_dir))

    mod_python_paths = [
        os.path.abspath(str(path))
        for path
        in py_dir.rglob("*")
        if path.is_dir() and path.name != "__pycache__"
    ]

    new_pythonpath += mod_python_paths

print("{sx}\nPITNONPATH List\n{sx}".format(sx="-" * 20))
for i in new_pythonpath:
    print(i)

print("{sx}\nPITNONPATH String\n{sx}".format(sx="-" * 20))
print(":".join(new_pythonpath))
