
import os
import sys
from pathlib import Path

build_dirs = [
    "Debug",
    "Release-symbols",
    "Release-light",
    "Release",
]


def add_assets(assets_path):
    # Add Assets dir
    if assets_path not in sys.path:
        print(assets_path)
        sys.path.append(assets_path)

    # Add Python dir
    assets_python = os.path.join(assets_path, "Python")
    if assets_python not in sys.path:
        print(assets_python)
        sys.path.append(assets_python)

    # Add Python/* subdirs
    for sub_path in Path(assets_python).rglob("*"):
        if sub_path.is_dir() and sub_path.name != "__pycache__":
            abs_sub_path = os.path.abspath(str(sub_path))
            if abs_sub_path not in sys.path:
                print(abs_sub_path)
                sys.path.append(abs_sub_path)


print("{sx}\nAdd PITNONPATH\n{sx}".format(sx="-" * 20))

# Add Core dir
if os.path.abspath("../CoreEngine") not in sys.path:
    print(os.path.abspath("../CoreEngine"))
    sys.path.append(os.path.abspath("../CoreEngine"))

# Add mod CvGameCoreDLL build dirs
if len(sys.argv) == 2:
    dll_path = os.path.abspath("../Mods/{}/CvGameCoreDLL".format(sys.argv[1]))
    if os.path.isdir(dll_path):
        for _dir in build_dirs:
            print(os.path.abspath(os.path.join(dll_path, "x64", "lin", _dir)))
            sys.path.append(os.path.abspath(os.path.join(dll_path, "x64", "lin", _dir)))
            print(os.path.abspath(os.path.join(dll_path, "x64", "win", _dir)))
            sys.path.append(os.path.abspath(os.path.join(dll_path, "x64", "win", _dir)))
    else:
        print("CvGameCoreDLL Mod Path '{}' not found".format(mod_path))


# Add mod Assets (if extists)
if len(sys.argv) == 2:
    mod_path = os.path.abspath("../Mods/{}/Assets".format(sys.argv[1]))
    if os.path.isdir(mod_path):
        add_assets(mod_path)
    else:
        print("Assets Mod Path '{}' not found".format(mod_path))


# Add game CvGameCoreDLL build dirs
if len(sys.argv) == 1:
    dll_path = os.path.abspath("../CvGameCoreDLL")
    for _dir in build_dirs:
        print(os.path.abspath(os.path.join(dll_path, "x64", "lin", _dir)))
        sys.path.append(os.path.abspath(os.path.join(dll_path, "x64", "lin", _dir)))
        print(os.path.abspath(os.path.join(dll_path, "x64", "win", _dir)))
        sys.path.append(os.path.abspath(os.path.join(dll_path, "x64", "win", _dir)))

# Add game Assets
add_assets(os.path.abspath("../Assets"))

print("{sx}\nImport CvPythonExtensions\n{sx}".format(sx="-" * 20))

from CvPythonExtensions import *

#print("{sx}\nImport CvPythonExtensions\n{sx}".format(sx="-" * 20))

import CvGameUtils
#import CvEventManager
