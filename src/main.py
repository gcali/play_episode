#! /usr/bin/env python3

from data import Data
import interface, find, play

class ChooseAction(Exception):
  def __init__(self, action, episode_name=None):
    self.action = action
    self.episode_name = episode_name

  def __str__(self):
    return repr(self.action)

def name_from_entry(entry):
    return "{0} - {1}x{2}".format(entry["name"],
                                  entry["season"], entry["episode"])

def handle_arrow_keys(entries, index, change, choices):
  if 0 <= index < len(entries):
    entries.change_episode(index, change)
    choices[index] = name_from_entry(entries[index])

def choose_episode(entries):
  choices = [name_from_entry(x) for x in entries]
  title = "Choose an episode"
  index = 0
  handle_left = lambda x,y: handle_arrow_keys(entries, y, -1, x)
  handle_right = lambda x,y: handle_arrow_keys(entries, y, +1, x)
  handlers = {"KEY_LEFT" : handle_left, "KEY_RIGHT" : handle_right}
  while True:
    (index,key) = interface.get_choice(title, choices,
                                       i=index, handlers=handlers)
    if key == "\n" or key == "KEY_ENTER":
      break
    elif key == "KEY_LEFT" and index != -1:
      entries.change_episode(index, -1)
      choices[index] = name_from_entry(entries[index])
    elif key == "KEY_RIGHT" and index != -1:
      entries.change_episode(index, +1)
      choices[index] = name_from_entry(entries[index])
    elif key == "q" or key == "KEY_F(3)":
      raise ChooseAction("quit")
    elif key == "KEY_F(2)":
      raise ChooseAction("save") 

  return index

def yes_or_no():
  choices = ["Yes", "No"]
  title = "Do you want to watch another episode?"
  index = 0
  while True:
    (index,key) = interface.get_choice(title, choices, i=index)
    if key == "y" or key == "Y":
      return True
    elif key == "n" or key == "N":
      return False
    elif key == "KEY_ENTER" or key == "\n":
      if index == 0:
        return True
      else:
        return False

if __name__ == "__main__":
  key = ""
  try:
    entries = Data()
    entries.get_data()
    interface.start()
    while True:
      try:
        entry_index=choose_episode(entries)
      except ChooseAction as e:
        if e.action == "save":
          entries.save_data()
          break
        elif e.action == "quit":
          break

      while True:
        try:
          episode = entries[entry_index]
          video_path = find.find_file(episode)
        except find.NotFoundError:
          interface.text_screen("File not found", True)
          break
        else:
            interface.text_screen("Enjoy the video!", False)
            play.play_video(video_path, "mplayer", "-zoom", "-ao", "alsa")
            entries.change_episode(entry_index,1)
            answ = yes_or_no()
            if not answ:
              break
  finally:
    interface.close()
