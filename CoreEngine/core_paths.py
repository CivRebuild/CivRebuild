
import os
from pathlib import Path
from core_config import constant


class CorePaths:

    def __init__(self, mod_name=os.environ.get("Civ_CONFIG_mod")):
        self.mod_name = mod_name
        self.root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def _add_assets2pythonpath(self, assets_path):
        # Add Assets dir
        self.python_path.append(assets_path)

        # Add Python dir
        assets_python = os.path.join(assets_path, constant.assets_python_dir)
        self.python_path.append(assets_python)

        # Add Python/* subdirs
        for sub_path in Path(assets_python).rglob("*"):
            if sub_path.is_dir() and sub_path.name != "__pycache__":
                abs_sub_path = os.path.abspath(str(sub_path))
                self.python_path.append(abs_sub_path)

    def get_pythonpath(self):
        self.python_path = []

        # Add Core dir
        engine_path = os.path.join(self.root_path, constant.engine_dir)
        self.python_path.append(engine_path)

        # Add mod CvGameCoreDLL build dirs
        if self.mod_name:
            dll_path = os.path.join(
                self.root_path,
                constant.mod_dir,
                self.mod_name,
                constant.sdk_dir,
            )
            if os.path.isdir(dll_path):
                for _dir in constant.sdk_build_dirs:
                    self.python_path.append(
                        os.path.abspath(os.path.join(dll_path, "x64", "lin", _dir))
                    )
                    self.python_path.append(
                        os.path.abspath(os.path.join(dll_path, "x64", "win", _dir))
                    )
            else:
                print("CvGameCoreDLL Mod Path '{}' not found".format(dll_path))

        # Add mod Assets (if extists)
        if self.mod_name:
            assets_path = os.path.join(
                self.root_path,
                constant.mod_dir,
                self.mod_name,
                constant.assets_dir,
            )
            if os.path.isdir(assets_path):
                self._add_assets2pythonpath(assets_path)
            else:
                print("Assets Mod Path '{}' not found".format(assets_path))

        # Add game CvGameCoreDLL build dirs
        dll_path = os.path.join(
            self.root_path,
            constant.sdk_dir,
        )
        for _dir in constant.sdk_build_dirs:
            self.python_path.append(
                os.path.abspath(os.path.join(dll_path, "x64", "lin", _dir))
            )
            self.python_path.append(
                os.path.abspath(os.path.join(dll_path, "x64", "win", _dir))
            )

        # Add game Assets
        assets_path = os.path.join(self.root_path, constant.assets_dir)
        self._add_assets2pythonpath(assets_path)

        return self.python_path

    def get_config_path(self):
        self.config_path = []

        return self.config_path

    def get_xml_path(self):
        self.xml_path = []

        return self.xml_path

