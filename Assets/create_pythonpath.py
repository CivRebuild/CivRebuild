
import os
from pathlib import Path


core_dir = os.path.abspath("../CoreEngine")
python_dirs = [
   Path(os.path.abspath("Python")),
]

new_pythonpath = []
new_pythonpath.append(os.path.abspath(core_dir))

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
