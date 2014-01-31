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
    (index,key) = interface.get_choice(title, *choices, i=index)
    if key == "\n" or key == "KEY_ENTER":
      break
    elif key == "KEY_LEFT" and index != -1:
      data.change_episode(entries, index, -1)
      choices[index] = name_from_entry(entries[index])
    elif key == "KEY_RIGHT" and index != -1:
      data.change_episode(entries, index, +1)
      choices[index] = name_from_entry(entries[index])
    elif key == "q" or key == "KEY_F(3)":
      raise ChooseAction("quit")
    elif key == "KEY_F(2)":
      raise ChooseAction("save") 

  return index

if __name__ == "__main__":
  key = ""
  try:
    entries = data.get_data()
    interface.start()
    while True:
      try:
        entry_index=choose_episode(entries)
        episode = entries[entry_index]
      except ChooseAction as e:
        if e.action == "save":
          data.save_data(entries)
          break
        elif e.action == "quit":
          break
      try:
        video_path = find.find_file(episode)
      except find.NotFoundError:
        interface.text_screen("File not found", True)
      else:
        interface.text_screen("Enjoy the video!", False)
        play.play_video(video_path, "mplayer", "-zoom", "-ao", "alsa")
        data.change_episode(entries,entry_index,1)
  finally:
    interface.close()
