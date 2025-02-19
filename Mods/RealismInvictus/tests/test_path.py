
import os
import sys
import doctest

os.environ["Civ_CONFIG_mod"] = "RealismInvictus"
sys.path.append(os.path.abspath("../../../CoreEngine"))

print("{sx}\nTEST Import CvPythonExtensions\n{sx}".format(sx="-" * 20))

from CvPythonExtensions import *

print("{sx}\nTEST Import CvGameUtils\n{sx}".format(sx="-" * 20))

import CvGameUtils

