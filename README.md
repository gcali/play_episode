play_episode
============

Python3 program to watch TV Series for Linux.

Quick Python program to play TV Series stored on the drive. The interface is ncurses based.

The program is able to store recently watched series and remember the last episode watched; every time an episode
is watched, the program procedes to ask if the next one should be played.

As of now, there's a time limit to answer the question; if no answer is given in 60 seconds, the program quits
with a return code of 2 (useful to implement a script to shutdown the PC in case no answer was given in time).

To add a new entry to the stored series, call the program from the directory where the files are and write
the name of the serie in the last line. Note: right now the program doesn't do any check about the file names, apart
from numerical ones to identify the correct season and episode. As a consequence, it should be called only in a directory
where there is only one series.
