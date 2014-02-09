#! /usr/bin/env python3

import re
import os
import errno

file_name = "play_episode.data"
base_dir = os.path.join(os.path.expanduser("~"),".play_episode") 

class RangeError(Exception):
  pass

class Data(list):
  
  def get_data(self):
    """Get the data about series already saved in the config file.

    The function looks for a file named as in "file_name" in
    these directories: the one in the environment variable
    "PLAY_EPISODE_DATA", if present; the current directory; the home of the
    user; the one in the variable "base_dir".
    If no suitable file is found, it creates a new one in "base_dir".
    The loaded file (or the newly created) is set as the default
    file by setting the variable "path"

    Returns:
      A list of dictionaries; each element of the list is a dictionary of 4
      elements, {name, season, episode, path}

    Raises:
      IOError: No suitable file was found, and a new file couldn't be
      created
    """ 
    del self[:]
    for loc in os.environ.get("PLAY_EPISODE_DATA"), os.curdir,\
               os.path.expanduser("~"), base_dir:
      try:
        with open(os.path.join(loc,file_name), "rU") as f:
          for line in f:
            self.append(_parse_line(line))
          self.path = os.path.join(loc,file_name)       
          break
      except IOError:
        pass
      except TypeError:
        pass
    else:
      _assure_dir(base_dir)
      with open(os.path.join(base_dir,file_name), "w"):
        pass

  def save_data(self):
    """Saves the current series data

    This function saves the current data to the file specified in "path".

    Raises:
      IOError: The file where to save the data in couldn't be opened
    """ 
    with open(self.path, "w") as f:
      for elem in self:
        for key in ("name","season","episode","path"): 
          f.write("{}|".format(elem[key]))
        f.write("\n")

  def add_entry(self, name, season, episode):
    conv_str = lambda x: str(x) if x >= 10 else "0" + str(x)
    season = conv_str(season)
    episode = conv_str(episode)
    self.append({"name":name, "season":season, "episode":episode,\
                 "path":os.path.abspath(os.curdir)})
    comp_fun = lambda x: x["name"].lower()
    self.sort(key=comp_fun)
    

  def change_path(self, new_path):
    """Changes the current default path
    """
    self.path = new_path

  def change_episode(self, index, shift):
    """Changes the value of the episode of an entry
    
    Changes the value of the episode of the entry number "index"
    to its old value plus "shift"; its value will always be between
    0 and 99.

    Args:
      index: The index of the entry to change
      shift: The value to add to the episode

    Raises:
      RangeError: No entry with the given index was found
    """

    val = int(self[index]["episode"])
    val = max(min(val+shift, 99),0)
    self[index]["episode"] = "{0:02d}".format(val)

def _parse_line(line):
  (name,season,episode,path) = \
    re.search(r"(.*?)\|(\d*?)\|(\d*?)\|(.*)\|", line).groups()
  return {"name":name, "season":season, "episode":episode, "path":path}


def _assure_dir(directory):
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
  data = Data()
  data.get_data() 
  data.add_entry("test", 1, 1)
  for list in data:
    print(list)
  data.change_episode(0, 1)
  for list in data:
    print(list)
  #save_data(data)
