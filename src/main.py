#! /usr/bin/env python3

import interface, data, find, play

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
      if e.key == "KEY_LEFT" and e.index != -1:
        data.change_episode(entries, e.index, -1)
        index = e.index
        choices[index] = name_from_entry(entries[index])
      elif e.key == "KEY_RIGHT" and e.index != -1:
        data.change_episode(entries, e.index, +1)
        index = e.index
        choices[index] = name_from_entry(entries[index])
      else:
        raise e
  return entries[index]

if __name__ == "__main__":
  key = ""
  try:
    entries = data.get_data()
    interface.start()
    i = 1
    while i > 0:
      try:
        video_path = find.find_file(choose_episode(entries))
      except interface.InputError as e:
        key = e.args[0]
      else:
        play.play_video(video_path, "mplayer", "-zoom", "-ao", "alsa")
      i -= 1
  finally:
    interface.close()
    print(key)
