import curses
import curses.panel

RULES = ['You have 10 ships. 4 single-deck, 3 double-deck, 2 three-deck and 1 four-deck',
         'Ships during deployment should not touch each other, there should be at least one cell between them',
         'Field size - 10 by 10',
         'Your task is to correctly place the ships on the field and win your opponent']
ABOUT_ME = ['My name is Max Siomin',
            '25 years',
            'Python Backend Developer',
            'Diligent and hardworking',
            'I love the x y coordinate system']

class Game:
    def __init__(self) -> None:
        pass



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
            if key in (curses.KEY_DOWN, ord('s')) and current_row < len(menu) - 1:
                current_row += 1
            if key == curses.KEY_ENTER or key in [10, 13]:
                if current_row == 0:
                    self._print_center("You won 1")
                elif current_row == 1:
                    self._print_rules()
                elif current_row == 2:
                    self._print_about()
                if current_row == len(menu) - 1:
                    break
                self.stdscr.getch()
            self._print_menu(current_row, menu)

    def _print_menu(self, curr_ind, menu):
        self.stdscr.clear()
        self.stdscr.border()
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

    def _print_rules(self):
        self.stdscr.clear()
        self.stdscr.border()
        h, w = self.stdscr.getmaxyx()
        for elem in range(len(RULES)):
            x = w//2 - len(RULES[elem])//2
            y = h//2 - len(RULES) + elem
            self.stdscr.addstr(y, x, RULES[elem])
            h, w = self.stdscr.getmaxyx()
            x = w//2
            y = h//2
        self.stdscr.addstr(y + 3, x - 15, 'Press enter to return in menu')

    def _print_about(self):
        self.stdscr.clear()
        self.stdscr.border()
        h, w = self.stdscr.getmaxyx()
        for elem in range(len(ABOUT_ME)):
            x = w//2 - len(ABOUT_ME[elem])//2
            y = h//2 - len(ABOUT_ME) + elem
            self.stdscr.addstr(y, x, ABOUT_ME[elem])
            h, w = self.stdscr.getmaxyx()
            x = w//2
            y = h//2
        self.stdscr.addstr(y + 3, x - 15, 'Press enter to return in menu')

    def _print_center(self, text):
        self.stdscr.clear()
        self.stdscr.border()
        h, w = self.stdscr.getmaxyx()
        x = w//2 - len(text)//2
        y = h//2
        self.stdscr.addstr(y, x, text)
        self.stdscr.refresh()


Menu()._start()
