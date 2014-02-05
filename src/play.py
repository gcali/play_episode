#! /usr/bin/env python3

import os
import subprocess

def play_video(video_path, player="mplayer", *opt,
               subtitle = None, sub_op = "-sub",
               suppress_output = True):
  """Plays a video
     
  This function plays a video, with an optional subtitle,
  with the player specified in "player".

  Args:
    video_path: A string with the path of the video to be played.
    player: Optional. The name of the executable used to play the video.
    *opt: Optional arguments to pass to the player, before the video.
    subtitle: Optional. If it's set to a string, that path is specified
              as the path of the subtitle file.
    sub_op: Optional. Used only if "subtitle" != None, the option to be
            passed to the player to specify the subtitle.
    suppress_output: Optional. If True, the standard output and
                     standard error are suppressed.
  """

  if subtitle != None:
    sub_part = [sub_op] + [subtitle]
  else:
    sub_part = []
  arg = [player] + list(opt) + [video_path] + sub_part
  if suppress_output:
    with open(os.devnull, "w") as FNULL:
      subprocess.call(arg, stdout=FNULL, stderr=FNULL)
  else:
    subprocess.call(arg)
  
if __name__ == "__main__":
  play_video("play_episode.data", player="cat", suppress_output=False)
  play_video("it", "echo", "Does", subtitle="?", sub_op = "work",
              suppress_output=False)
