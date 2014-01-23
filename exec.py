#! /usr/bin/env python3

import subprocess

def play_video(video_path, player="echo", *opt,
               subtitle = None, sub_op = "-sub"):
  if subtitle != None:
    sub_part = [sub_op] + [subtitle]
  else:
    sub_part = []
  arg = [player] + list(opt) + [video_path] + sub_part
  subprocess.call(arg)
  
if __name__ == "__main__":
  play_video("play_episode.data", player="echo", subtitle="test")
