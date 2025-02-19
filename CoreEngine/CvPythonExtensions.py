
import os
import sys
from pathlib import Path
from core_config import constant


# Add Python Paths

mod_name = os.environ.get("Civ_CONFIG_mod")
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

pythonpath_log = []


def add_assets(assets_path):
    # Add Assets dir
    if assets_path not in sys.path:
        sys.path.append(assets_path)
        pythonpath_log.append(assets_path)

    # Add Python dir
    assets_python = os.path.join(assets_path, constant.assets_python_dir)
    if assets_python not in sys.path:
        sys.path.append(assets_python)
        pythonpath_log.append(assets_python)

    # Add Python/* subdirs
    for sub_path in Path(assets_python).rglob("*"):
        if sub_path.is_dir() and sub_path.name != "__pycache__":
            abs_sub_path = os.path.abspath(str(sub_path))
            if abs_sub_path not in sys.path:
                sys.path.append(abs_sub_path)
                pythonpath_log.append(abs_sub_path)


# Add Core dir
engine_path = os.path.join(root_path, constant.engine_dir)
if engine_path not in sys.path:
    sys.path.append(engine_path)
    pythonpath_log.append(engine_path)

# Add mod CvGameCoreDLL build dirs
if mod_name:
    dll_path = os.path.join(
        root_path,
        constant.mod_dir,
        mod_name,
        constant.sdk_dir,
    )
    if os.path.isdir(dll_path):
        for _dir in constant.sdk_build_dirs:
            sys.path.append(os.path.abspath(os.path.join(dll_path, "x64", "lin", _dir)))
            pythonpath_log.append(os.path.abspath(os.path.join(dll_path, "x64", "lin", _dir)))

            sys.path.append(os.path.abspath(os.path.join(dll_path, "x64", "win", _dir)))
            pythonpath_log.append(os.path.abspath(os.path.join(dll_path, "x64", "win", _dir)))
    else:
        print("CvGameCoreDLL Mod Path '{}' not found".format(dll_path))


# Add mod Assets (if extists)
if mod_name:
    assets_path = os.path.join(
        root_path,
        constant.mod_dir,
        mod_name,
        constant.assets_dir,
    )
    if os.path.isdir(assets_path):
        add_assets(assets_path)
    else:
        print("Assets Mod Path '{}' not found".format(assets_path))


# Add game CvGameCoreDLL build dirs
if not mod_name:
    dll_path = os.path.join(
        root_path,
        constant.sdk_dir,
    )
    for _dir in constant.sdk_build_dirs:
        sys.path.append(os.path.abspath(os.path.join(dll_path, "x64", "lin", _dir)))
        pythonpath_log.append(os.path.abspath(os.path.join(dll_path, "x64", "lin", _dir)))

        sys.path.append(os.path.abspath(os.path.join(dll_path, "x64", "win", _dir)))
        pythonpath_log.append(os.path.abspath(os.path.join(dll_path, "x64", "win", _dir)))

# Add game Assets
add_assets(os.path.join(root_path, constant.assets_dir))


if pythonpath_log:
    print("{sx}\nAdd PITNONPATH\n{sx}".format(sx="-" * 20))
    for path_log in pythonpath_log:
        print(path_log)

# Base Import

print("{sx}\nCore Init\n{sx}".format(sx="-" * 20))

from CvPythonEngine import *
from CvGameCoreDLL import *
