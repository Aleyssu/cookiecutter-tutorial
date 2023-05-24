import re
import sys
import os


MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9 ]+$'

project_name = '{{ cookiecutter.project_name }}'

if not re.match(MODULE_REGEX, project_name):
    print('ERROR: %s is not a valid project name!' % project_name)

    # exits with status 1 to indicate failure
    sys.exit(1)