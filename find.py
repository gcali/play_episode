#! /usr/bin/env python3

import os
import re
import data

set_extensions = set(("mkv","avi","mp4"))

if __name__ == "__main__":
  data_list = data.get_data()
  for elem in data_list:
    os.chdir(elem[3])
    for line in sorted(os.listdir()):
      for ext in set_extensions:
        expr=r".*{0}[xXeE]{1}.*\.{2}$".format(int(elem[1]),elem[2],ext)
        if re.match(expr, line):
          print(line)
