
import os
import sys
from pathlib import Path


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

# Add mod Assets (if extists)
if len(sys.argv) == 2:
    mod_path = os.path.abspath("../Mods/{}/Assets".format(sys.argv[1]))
    if os.path.isdir(mod_path):
        add_assets(mod_path)
    else:
        print("Assets Mod Path '{}' not found".format(mod_path))

# Add game Assets
add_assets(os.path.abspath("../Assets"))

print("{sx}\nImport CvPythonExtensions\n{sx}".format(sx="-" * 20))

from CvPythonExtensions import *

#print("{sx}\nImport CvPythonExtensions\n{sx}".format(sx="-" * 20))

#import CvEventManager
