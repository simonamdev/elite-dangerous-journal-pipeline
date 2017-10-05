import sys
from cx_Freeze import setup, Executable

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

setup(name='edjp-app',
      version='0.1',
      description='Elite: Dangerous Journal Pipeline App',
      executables=[Executable('pipeline_app.py', base=base)])
