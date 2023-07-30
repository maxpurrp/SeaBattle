import curses


class Menu:
    def __init__(self) -> None:
        self.stdscr = curses.initscr()

    def _start(self):
        menu = ['PLAY GAME', 'RULES', 'ABOUT', 'EXIT']

        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.stdscr.border()
        current_row = 0
        self._print_menu(current_row, menu)
        while True:
            self.stdscr.keypad(1)
            key = self.stdscr.getch()
            if key in (curses.KEY_UP, ord('w')) and current_row > 0:
                current_row -= 1
            if key in (curses.KEY_DOWN, ord('s')) and current_row < len(menu)-1:
                current_row += 1
            if key == curses.KEY_ENTER or key in [10, 13]:
                self._print_center("You won")
                self.stdscr.getch()
                if current_row == len(menu) - 1:
                    break
            self._print_menu(current_row, menu)

    def _print_menu(self, curr_ind, menu):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        for idx, elem in enumerate(menu):
            x = w//2 - len(elem)//2
            y = h//2 - len(menu)//2 + idx
            if idx == curr_ind:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y, x, elem)
                self.stdscr.attroff(curses.color_pair(1))
            else:
                self.stdscr.addstr(y, x, elem)

    def _print_center(self, text):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        x = w//2 - len(text)//2
        y = h//2
        self.stdscr.addstr(y, x, text)
        self.stdscr.refresh()


Menu()._start()
