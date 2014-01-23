#! /usr/bin/env python3

import interface, data, find, play

def name_from_entry(entry):
    return "{0} - {1}x{2}".format(entry["name"],
                                  entry["season"], entry["episode"])

def choose_episode(entries):
  choices = [name_from_entry(x) for x in entries]
  title = "Choose an episode"
  return entries[interface.get_choice(title, *choices)]

if __name__ == "__main__":
  try:
    entries = data.get_data()
    interface.start()
    i = 1
    while i > 0:
      video_path = find.find_file(choose_episode(entries))
      play.play_video(video_path, "mplayer", "-zoom")
      i -= 1
  finally:
    interface.close()
