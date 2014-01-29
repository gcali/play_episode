#! /usr/bin/env python3

import curses


margin_up = 0
margin_left = 1

class TimeError(Exception):
  """Exception to be used to mean an operation took too much time"""
  pass

class InputError(Exception):
  """Exception to be used if a not meaningful key is pressed
     in get_choice.
     
  Attributes:
    self.key: The pressed key
    self.index: Optional. The index of the entry that was being
                selected when the key was pressed"""
  def __init__(self, key, index=-1):
    self.key = key
    self.index = index

  def __str__(self):
    return repr(self.key)

class Window:
  """Abstraction of a window.

  Used as a wrapper to use a window with ncurses.

  Attributes:
    start_row: The vertical offset of the window.
    start_col: The horizontal offset of the window.
    dim_row: The number of lines of the window.
    dim_col: The number of columns of the window.
    win: If necessary, the actual ncurses window associated with the object.
  """
  def __init__(self, dim_row, dim_col = -1,\
                     start_row = 0, start_col = 0):
    """Initiates a new window.

    Initiates a new window of "dim_row" lines, with optional arguments
    to specify offsets and width

    Args:
      dim_row: The number of lines of the window.
      dim_col: Optional. The number of columns of the window. Default value: the entire
               screen.
      start_row: Optional. The vertical offset of the window. 
      start_col: Optional. The horizontal offset of the window.
    """

    if dim_col == -1:
      dim_col = stdscr.getmaxyx()[1] - margin_left
    start_row += margin_up
    start_col += margin_left
    self.win = curses.newwin(dim_row, dim_col, start_row, start_col)
    self.win.keypad(True)
    self.dim_row, self.dim_col, self.start_row, self.start_col =\
    dim_row, dim_col, start_row, start_col
    self.full = False

  def print_str(self, *args):
    """Prints a new string in the window.

    Note: the string isn't actually displayed until the next call to
    refresh().

    Args:
      [y,x]: Optional. The first two arguments are optional, and stand respectively
             for the vertical and horizontal offset chosen for the string.
      string: The string to be printed.
      [attr]: Optional. Another optional argument, the attribute to be passed. Different
              attributes can be ORed. Not comprehensive possible values:
              A_REVERSE: Highlight the string
              A_BOLD: The string is printed in bold character
    
    Raises:
      curses.error: Curses raised an error when the string was printed.
    """
    try:
      self.win.addstr(*args)
    except curses.error:
      self.full = True
      close()
      raise
    else:
      self.full = False

  def get_char(self, *args):
    """Gets a char from the input.

    Returns a string representing the first character in the input queue.
    Special characters are spelled out (e.g. "KEY_BACKSPACE", "KEY_ENTER").  

    Args:
      Currently not to be used.

    Returns:
      The input string.
    """
    return self.win.getkey(0,0,*args)

  def clear(self):
    """Clears the window.

    Removes any printed character from the window. Note: the window isn't
    actually cleared until the next call to refresh()
    """
    return self.win.clear()

  def refresh(self):
    """Refreshes the window.

    Displays any change made to the window since the last call to
    refresh().
    """
    return self.win.refresh()

  def create_under(self, dim_row, dim_col = -1,
                         diff_row = 0, start_col = 0):
    """Creates a new window under the current one.

    Creates a new window of "dim_row" lines under the current one, with optional
    offsets and width.

    Args:
      dim_row: The number of lines of the new window.
      dim_col: Optional. The number of columns of the new window.
               Default value: The entire screen.
      diff_row: Optional. The vertical offset of the new window from the
                current one.
      start_col: Optional. The horizontal offset of the new window.

    Returns:
      The new window.
    """
    start_row = self.dim_row + self.start_row + diff_row
    return Window(dim_row, dim_col, start_row, start_col)

    
def start():
  """Initializes curses.
  """
  global stdscr
  global win_input
  global get_char

  stdscr = curses.initscr()
  curses.noecho()
  curses.cbreak()
  stdscr.keypad(True)
  curses.curs_set(False)
  stdscr.clear()
  stdscr.refresh()
  win_input = Window(1,1, curses.LINES-1, curses.COLS-1)
  get_char = win_input.get_char

def close():
  """Closes ncurses.

  Closes ncurses and ripristinates shell mode.
  """
  curses.nocbreak()
  stdscr.keypad(False)
  curses.echo()
  curses.endwin()

def clear_screen():
  """Clears the screen"""
  stdscr.clear()
  stdscr.refresh()

def choice_screen(title, *choices, high=-1, start_row = 0, start_col = 0):
  """Creates a new window to choose from a number of alternatives.

  Creates a new window object with a line for a title and the arguments in "choices"
  as possible choices. Highlights a line if it's specified. The window needs not
  to be refreshed to display the screen.

  Args:
    title: The title of the screen.
    *choices: The lines to be printed as choices beneath the title.
    high: Optional. The line to highlight. If it's out of range, no line is highlighted.
    start_row: Optional. The vertical offset of the new window.
    start_col: Optional. The horizontal offset of the new window.

  Returns:
    The new window.
  """
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

def get_choice(title, *choices, get_input = False, time = -1, i = 0):
  """Makes the user choose between a number of choices.

  Calls choice_screen() with the given choices, and returns the index of
  the chosen line. If "get_input" is True, adds a blank line where the
  user can write a new choice, and returns a tuple with the index of the
  chosen line and any input written in the new line. The user can confirm
  his choice by pressing Enter. If "time" is greater than -1, if the user
  doesn't provide any input in "time" tenth of seconds, an exception is
  raised. If a user does provide some input, but is too slow in doing it,
  an exception could still be raised; this behaviour should be fixed.

  Args:
    title: The title of the screen.
    *choices: The lines to be printed as choices beneath the title.
    get_input: Optional. If set to true, adds a new blank line to the bottom
               of the screen to be used to write a new choice and alters the
               return value.
    time: Optional. If time >= 0, wait up to time tenths of a second for an
          answer. If no answer is given, raises TimeError
    i: Optional. Currently selected line.

  Raises:
    TimeError: No input was given in time 
    InputError: The given input isn't recognized by the function.
                The "index" attribute is set to the current selected
                line, which is -1 if it's the input one

  Returns:
    If "get_input" is False, the index of the selected line.
    If "get_input" is True, a tuple with the index of the selected line and
    a string containing any input written in the new line.
  """
  new_input = ""
  n_lines = len(choices)
  if get_input:
    max_i = n_lines
  else:
    max_i = n_lines-1
  min_i = 0
  delay = lambda x: 255 if x > 255 else x % 256
  if time >= 0:
    curses.halfdelay(delay(time))
  while True:
    screen = choice_screen(title, *(choices + (new_input,)), high=i)
    try:
      c = get_char()
    except curses.error:
      if time < 255:
        curses.cbreak()
        clear_screen()
        raise TimeError
      else:
        time -= 255
        curses.halfdelay(delay(time))
        c = None

    if c == None:
      pass
    elif c == "KEY_DOWN":
      i = min(i+1,max_i)
    elif c == "KEY_UP":
      i = max(i-1,min_i)
    elif c == "\n" or c == "KEY_ENTER":
      break
    elif get_input and i == max_i:
      if c.isalpha():
        new_input += c
      elif c == "KEY_BACKSPACE":
        new_input = new_input[:-1]
      else:
        raise InputError(c)
    else:
      raise InputError(c, i)

  curses.cbreak()
  clear_screen()
    
  if get_input:
    return (i, new_input)
  else:
    return i


if __name__ == "__main__":
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
  try:
    i, junk = get_choice(title, *choices, get_input = True, time = 20) 
  except TimeError:
    choices = f("Ok ", 0,5)
    i, junk = get_choice(title, *choices, get_input = True)
  

  close()

  print(win.dim_row, win.dim_col, win.start_row, win.start_col)
  print(char)
  print(i, junk)
