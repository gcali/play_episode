#! /usr/bin/env python3

import os

print(os.path.join(os.path.expanduser("~") + "/", "temp_file"))

print(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
