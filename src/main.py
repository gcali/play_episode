#! /usr/bin/env python3

import interface, data, find, play

class ChooseAction(Exception):
  def __init__(self, action, episode_name=None):
    self.action = action
    self.episode_name = episode_name

  def __str__(self):
    return repr(self.action)

def name_from_entry(entry):
    return "{0} - {1}x{2}".format(entry["name"],
                                  entry["season"], entry["episode"])

def choose_episode(entries):
  choices = [name_from_entry(x) for x in entries]
  title = "Choose an episode"
  index = 0
  while True:
    try:
      index = interface.get_choice(title, *choices, i=index)
      break
    except interface.InputError as e:
      index = e.index
      if e.key == "KEY_LEFT" and e.index != -1:
        data.change_episode(entries, e.index, -1)
        choices[index] = name_from_entry(entries[index])
      elif e.key == "KEY_RIGHT" and e.index != -1:
        data.change_episode(entries, e.index, +1)
        choices[index] = name_from_entry(entries[index])
      elif e.key == "q" or e.key == "KEY_F(3)":
        raise ChooseAction("quit")
      elif e.key == "KEY_F(2)":
        raise ChooseAction("save") 

  return entries[index]

if __name__ == "__main__":
  key = ""
  try:
    entries = data.get_data()
    interface.start()
    i = 1
    while i > 0:
      try:
        episode=choose_episode(entries)
      except ChooseAction as e:
        if e.action == "save":
          break
        elif e.action == "quit":
          break
      try:
        video_path = find.find_file(episode)
      except find.NotFoundError:
        #TODO Implement file not found screen 
        pass
      else:
        play.play_video(video_path, "mplayer", "-zoom", "-ao", "alsa")
      i -= 1
  finally:
    interface.close()
