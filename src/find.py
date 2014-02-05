#! /usr/bin/env python3

import os
import re
import data

set_extensions = set(("mkv","avi","mp4"))

class _FoundError(Exception):
  pass
class NotFoundError(Exception):
  """Raised in find_file if no file is found"""
  pass

def gen_expr(season,episode,extension):
  """Generates the regular expression for the file"""
  return r".*0*{0}[xXeE]0*{1}.*\.{2}$".format(int(season),
                                              int(episode),
                                              extension)

def find_file(entry, find_subs = False):
  """Finds a path for a file based on entry

  This function takes from an "entry" variable the data to
  return a string containing a path to the best matching episode.
  As of now, "mkv" files are preferred to "mp4", which are preferred
  to "avi". If "find_subs" is True, returns a tuple with a suitable
  subtitle path as the second element, or None.

  Args:
    entry:  A container-like variable with at least four elements:
            entry["name"] is the name of the series
            entry["season"], entry["episode"] are the number of the season
              and the episode
            entry["path"] is the path in which to look for the episode
    find_subs:  If True and a file name was found, returns a tuple with
                the path with the corresponding subtitles, if found, None
                otherwise.

  Raises:
    NotFoundError: No suitable match for the given entry was found

  Return:
    If an episode was found, returns the path of the episode. If "find_subs"
    is True, returns a tuple with the path of the episode as the first
    element, and the path to the subtitle (or None, if no subtitle was
    found) as the second.
  """
  os.chdir(entry["path"])
#  gen_expr = lambda x: r".*0*{0}[xXeE]0*{1}.*\.{2}$".format(
#    int(entry["season"]), int(entry["episode"]), x
#  )
  try:
    for ext in set_extensions:
      expr = gen_expr(entry["season"], entry["episode"], ext)
      for name in sorted(os.listdir()):
        if re.match(expr,name):
          raise _FoundError
    else:
      raise NotFoundError
  except _FoundError:
    if not find_subs:
      return name

  expr = gen_expr(entry["season"], entry["episode"], "srt")
  for sub in sorted(os.listdir()):
    if re.match(expr,sub):
      return (name,sub)
  else:
    return (name,None)
    

if __name__ == "__main__":
  data_list = data.get_data()
  for elem in data_list:
    name = find_file(elem, True)
    print(name)
