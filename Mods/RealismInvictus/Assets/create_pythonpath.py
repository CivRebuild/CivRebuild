
import os
import sys

sys.path.append(os.path.abspath("../../../CoreEngine"))
from core_paths import CorePaths

cor_pat = CorePaths("RealismInvictus")
pythonpath = cor_pat.get_pythonpath()

print("{sx}\nPITNONPATH List\n{sx}".format(sx="-" * 20))
for i in pythonpath:
    print(i)

print("{sx}\nPITNONPATH String\n{sx}".format(sx="-" * 20))
print(":".join(pythonpath))
