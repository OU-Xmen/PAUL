import os
from importlib.machinery import SourceFileLoader
maindirectory = os.path.dirname(os.path.abspath(__file__))
PaulFunc = SourceFileLoader('top_secret_paul_function', os.path.join(maindirectory, 'paul\'s secret directory\\top_secret_paul_function.py')).load_module() # from common path

PaulFunc.paul_is_watching()