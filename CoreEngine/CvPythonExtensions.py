
import sys
from core_paths import CorePaths

cor_pat = CorePaths()
pythonpath = cor_pat.get_pythonpath()

pythonpath_log = []
for path in pythonpath:
    if path not in sys.path:
        sys.path.append(path)
        pythonpath_log.append(path)

if pythonpath_log:
    print("{sx}\nAdd PITNONPATH\n{sx}".format(sx="-" * 20))
    for path_log in pythonpath_log:
        print(path_log)


print("{sx}\nCore Init\n{sx}".format(sx="-" * 20))
from CvPythonEngine import *
from CvGameCoreDLL import *
