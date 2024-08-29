# conftest.py
import sys

# For convenience we add these relative paths to allow running pytest from 
# the app root directory or the tests subdirectory.
src_paths = ['../src', './src']
for path in src_paths:
    sys.path.append(path)

