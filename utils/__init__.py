"""Import modules from other packages for a common reference."""

import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)
if PROJECT_DIR not in sys.path:
    sys.path.append(PROJECT_DIR)


from .containers import flatten_list, flatten_dict, \
     ensure_dict, ensure_list, \
     RecordDict
from .textutils import TextCleaner
