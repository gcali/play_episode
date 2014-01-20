#! /usr/bin/env python3

import curses

stdscr = curses.initscr()

margin_up = 0
margin_left = 1

class Window:
  def __init__(self, dim_row, dim_col = curses.LINES - margin_left,\
                     start_row = 0, start_col = 0):
    start_row += margin_up
    start_col += margin_left
    self.win = curses.newwin(dim_row, dim_col, start_row, start_col)
    self.win.keypad(True)
    self.dim_row, self.dim_col, self.start_row, self.start_col =\
    dim_row, dim_col, start_row, start_col
    self.full = False

  def print_str(self, *args):
    try:
      self.win.addstr(*args)
    except curses.error:
      self.full = True
      close()
      raise
    else:
      self.full = False

  def get_char(self, *args):
    return self.win.getkey(0,0,*args)

  def clear(self):
    return self.win.clear()

  def refresh(self):
    return self.win.refresh()

  def create_under(self, dim_row, dim_col = curses.LINES - margin_left,
                         diff_row = 0, start_col = 0):
    start_row = self.dim_row + self.start_row + diff_row
    return Window(dim_row, dim_col, start_row, start_col)

    
def start():
  global win_input
  global get_char

  curses.noecho()
  curses.cbreak()
  stdscr.keypad(True)
  curses.curs_set(False)
  stdscr.clear()
  stdscr.refresh()
  win_input = Window(1,1, curses.LINES-1, curses.COLS-1)
  get_char = win_input.get_char

def close():
  curses.nocbreak()
  stdscr.keypad(False)
  curses.echo()
  curses.endwin()

def choice_screen(title, *choices, high=-1, start_row = 0, start_col = 0):
  screen = Window(2 + len(choices) + 1, start_row = start_row, start_col = start_col)
  screen.print_str(title + "\n\n", curses.A_BOLD)
  pad = len(max(choices,key=len))
  for i,line in enumerate(choices):
    if i == high:
      screen.print_str(line.ljust(pad) + "\n", curses.A_REVERSE)
    else:
      screen.print_str(line.ljust(pad) + "\n")
  screen.refresh()
  return screen

def get_choice(title, *choices, get_input = False, i = 0):
  new_input = ""
  n_lines = len(choices)
  if get_input:
    max_i = n_lines
  else:
    max_i = n_lines-1
  min_i = 0
  while True:
    screen = choice_screen(title, *(choices + (new_input,)), high=i)
    c = get_char()
    if c == "KEY_DOWN":
      i = min(i+1,max_i)
    elif c == "KEY_UP":
      i = max(i-1,min_i)
    elif c == "\n" or c == "KEY_ENTER" or c == "q":
      break
    elif get_input and i == max_i:
      if c.isalpha():
        new_input += c
      elif c == "KEY_BACKSPACE":
        new_input = new_input[:-1]
    
  if get_input:
    return (i, new_input)
  else:
    return i


start() 


win = Window(10,10)
win = win.create_under(2)

win.print_str("prova")
win.refresh()
char = get_char()

win.clear()
win.refresh()


title = "Prova"
f = lambda s,x,y: [s + str(i) for i in range(x,y+1)]
choices = f("Linea ", 0, 10)
i, junk = get_choice(title, *choices, get_input = True) 

close()

print(win.dim_row, win.dim_col, win.start_row, win.start_col)
print(char)
print(i, junk)
