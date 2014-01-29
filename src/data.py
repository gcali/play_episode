#! /usr/bin/env python3

import re
import os
import errno

file_name = "play_episode.data"
base_dir = os.path.join(os.path.expanduser("~"),".play_episode") 
path = os.path.join(base_dir,file_name)

#print(os.path.join(base_dir,file_name))

class RangeError(Exception):
  pass

def get_data():
  """Get the data about series already saved in the config file.

  The function looks for a file named as in "file_name" in
  these directories: the one in the environment variable "PLAY_EPISODE_DATA",
  if present; the current directory; the home of the user; the one in
  the variable "base_dir".
  If no suitable file is found, it creates a new one in "base_dir".
  The loaded file (or the newly created) is set as the default
  file by setting the variable "path"

  Returns:
    A list of lists; each element of the list is a list of 4 elements,
    [name, season, episode, path].

  Raises:
    IOError: No suitable file was found, and a new file couldn't be created
  """ 
  global path

  data = []
  for loc in os.environ.get("PLAY_EPISODE_DATA"), os.curdir, os.path.expanduser("~"), base_dir:
    try:
      with open(os.path.join(loc,file_name), "rU") as f:
        for line in f:
          data.append(_parse_line(line))
          #data.append(tuple([x for x in _parse_line(line)]))
        path = os.path.join(loc,file_name)       
        break
    except IOError:
      pass
    except TypeError:
      pass
  else:
    assure_dir(base_dir)
    with open(os.path.join(base_dir,file_name), "w"):
      pass

  return data

def _parse_line(line):
  (name,season,episode,path) = \
    re.search(r"(.*?)\|(\d*?)\|(\d*?)\|(.*)\|", line).groups()
  return {"name":name, "season":season, "episode":episode, "path":path}


def save_data(data):
  """Saves the current series data

  This function saves the data from the variable "data" to the
  file specified in "path".

  Args:
    data: A list of dictionaries of 4 elements of the format
          {"name":,"season":,"episode":,"path":}

  Raises:
    IOError: The file where to save the data in couldn't be opened
  """ 
  with open(path, "w") as f:
    for elem in data:
      for key in ("name","season","episode","path"): 
        f.write("{}|".format(elem[key]))
      f.write("\n")

def change_episode(data, index, shift):
  """Changes the value of the episode of an entry
  
  Changes the value of the episode of the entry number "index"
  to its old value plus "shift"; its value will always be between
  0 and 99.

  Args:
    data: The data to change.
    index: The index of the entry to change
    shift: The value to add to the episode

  Raises:
    RangeError: No entry with the given index was found"""

  val = int(data[index]["episode"])
  val = max(min(val+shift, 99),0)
  data[index]["episode"] = "{0:02d}".format(val)


def assure_dir(directory):
  """Assures of the existance of "directory"
  Creates a new directory in "directory" if it isn't already
  there.

  Args:
    directory: The path of the directory to be created.

  Raises:
    OSError: The directory couldn't be created, either because
             of privileges or because a non-directory file of the
             same name already exists
  """
  try:
    os.makedirs(directory)
  except OSError as exception:
    if exception.errno != errno.EEXIST or not os.path.isdir(base_dir):
      raise
  

if __name__ == "__main__":
  data = get_data() 
  for list in data:
    print(list)
  change_episode(data, 0, 1)
  for list in data:
    print(list)
  #save_data(data)
