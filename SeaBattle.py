import pygame
from config import RULES, ABOUT_ME, MODES, MENU, HEIGHT, WIDGHT, NAME, WHITE, BLACK, SHIPS


class Game:
    def __init__(self, mode) -> None:
        self.game = pygame
        self.game.init()
        self.screen = pygame.display.set_mode((HEIGHT, WIDGHT), flags=pygame.NOFRAME)
        self.user_fild = self.game.draw.rect(self.screen, (71, 76, 112), (15, 15, 260, 260))
        self.surface = self.game.font.SysFont('arial', 18)
        self.mode = mode
        self.letters = [self.surface.render(elem, True,
                                            (255, 255, 255)) for elem in 'ABCDEFGHIJ']
        self.nums = [self.surface.render(str(elem), True,
                                         (255, 255, 255)) for elem in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
        self.ships = SHIPS
        self.block_size = 24
        self.left_marg = 40
        self.upper_marg = 50
        self.menu_ind = 0
        self.font_size = int(self.block_size / 1.5)
        self.font = self.game.font.SysFont('notosize', self.font_size)
        self.ships_on_fiend = []

    def start(self):
        self.screen.fill(BLACK)
        self.draw_field()
        while True:
            for event in pygame.event.get():
                if event.type == self.game.KEYDOWN:
                    if event.key == self.game.K_BACKSPACE:
                        exit()
                    if event.key == self.game.K_w or event.key == self.game.K_UP:
                        self._switch_ind(-1)
                    if event.key == self.game.K_s or event.key == self.game.K_DOWN:
                        self._switch_ind(1)
                    if event.key == self.game.K_RETURN:
                        self.draw_ship(4 - self.menu_ind)
                        self.ships[list(self.ships.keys())[self.menu_ind]] = self.ships[list(self.ships.keys())[self.menu_ind]] - 1


            self.select_ship()
            self.game.display.update()

    def draw_ship(self, ship):
        print(ship)
        x, y = self.left_marg, self.upper_marg + 12 * self.block_size
        while True:
            start_pos = self.game.Rect(x, y ,self.block_size * ship + 1,self.block_size + 1)
            for event in self.game.event.get():
                if event.type == self.game.KEYDOWN:
                    if event.key == self.game.K_BACKSPACE:
                        self.draw_field()
                        return
                    if event.key == self.game.K_LEFT or event.key == self.game.K_a:
                        if x <= 40:
                            pass
                        else:
                            x -= 24
                    if event.key == self.game.K_RIGHT or event.key == self.game.K_d:
                        if x + (ship - 1) * self.block_size >= 256:
                            pass
                        else:
                            x += 24
                    if event.key == self.game.K_w or event.key == self.game.K_UP:
                        if y <= 338:
                            pass
                        else:
                            y -= 24
                    if event.key == self.game.K_s or event.key == self.game.K_DOWN:
                        if y >= 554:
                            pass
                        else:
                            y += 24
                    if event.key == self.game.K_RETURN:
                        # coordinate
                        print((x // 24, (y  // 24) - 13), ((x // 24) + ship - 1, (y  // 24) - 13)) # from to
                        self.ships_on_fiend.append(start_pos)
                        self.draw_field()
                        return

            self.draw_field()
            self.game.draw.rect(self.screen, (255, 0, 0), self.game.Rect(start_pos), 1)
            self.game.display.update()

    def select_ship(self):
        self.game.draw.rect(self.screen, BLACK, (600, 300, 800, 800))
        for i, ship in enumerate(list(self.ships.keys())):
            count_ships = self.ships[ship]
            if count_ships > 0:
                ship = self.surface.render(f'{count_ships}x {ship}', True, WHITE)
            else:
                #self.ships.pop(ship)
                continue
            ship_rect = ship.get_rect()
            ship_rect.center = (700, 330 + i * 25)
            if i == self.menu_ind:
                self.game.draw.rect(self.screen, (96, 116, 120), ship_rect)
            self.screen.blit(ship, ship_rect)

    def draw_field(self):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        title = self.font.render(self.mode, 1, WHITE)
        for y in range(11):
            for x in range(11):
                # first field
                self.game.draw.line(self.screen, WHITE, (self.left_marg,self.upper_marg + y * self.block_size),
                                    (self.left_marg + 10 * self.block_size, self.upper_marg + y * self.block_size), 1)
                self.game.draw.line(self.screen, WHITE, (self.left_marg + x * self.block_size,self.upper_marg),
                                    (self.left_marg + x * self.block_size,self.upper_marg + 10 * self.block_size), 1)
                # second field
                self.game.draw.line(self.screen, WHITE, (self.left_marg,(self.upper_marg + y * self.block_size) + 12 * self.block_size),
                                    (self.left_marg + 10 * self.block_size, (self.upper_marg + y * self.block_size)+ 12 * self.block_size), 1)
                self.game.draw.line(self.screen, WHITE, (self.left_marg + x * self.block_size,self.upper_marg + 12 * self.block_size),
                                    (self.left_marg + x * self.block_size,self.upper_marg + 22 * self.block_size), 1)
            if y < 10:
                num = self.font.render(str(y + 1), 1, WHITE)
                char = self.font.render(letters[y], 1, WHITE)
                
                num_widht = num.get_width()
                num_height = num.get_height()

                char_widht = char.get_width()
                # first field
                self.screen.blit(num, (self.left_marg - (self.block_size//2 + num_widht // 2), self.upper_marg + y * self.block_size + (self.block_size // 2 - num_height // 2)))
                self.screen.blit(char, (self.left_marg + y *self.block_size + (self.block_size // 2 - char_widht // 2), (self.upper_marg + 10 * self.block_size) + 5))
                # second field
                self.screen.blit(num, (self.left_marg - (self.block_size//2 + num_widht // 2), (self.upper_marg + y * self.block_size + (self.block_size // 2 - num_height // 2) + 12 * self.block_size)))
                self.screen.blit(char, (self.left_marg + y *self.block_size + (self.block_size // 2 - char_widht // 2), ((self.upper_marg + 10 * self.block_size) + 5) + 12 * self.block_size))
        title = self.surface.render(f'MODE : {self.mode}', 1, WHITE)
        head = title.get_rect()
        head.center = (HEIGHT // 2, WIDGHT // 10)
        self.screen.blit(title, head)
        if self.ships_on_fiend:
            for elem in self.ships_on_fiend:
                elem[0] += 1
                elem[1] += 1
                elem[2] -= 2
                elem[3] -= 2
                self.game.draw.rect(self.screen, (105, 128, 255), elem)
        if len(self.ships_on_fiend) == 10:
            print('lets go')

    def _switch_ind(self, num):
        self.menu_ind = max(0, min(self.menu_ind + num, len(self.ships) - 1))


class Menu:

    def __init__(self) -> None:
        self.game = pygame
        self.game.init()
        self.screen = pygame.display.set_mode((HEIGHT, WIDGHT), flags=pygame.NOFRAME)
        self.surface = self.game.font.SysFont('arial', 35)
        self.back_font = self.game.font.SysFont('aroal', 25)
        self.rules_font = self.game.font.SysFont('arial', 17)
        self.options = [self.surface.render(elem, True, (255, 255, 255)) for elem in MENU]
        self.about_me = [self.surface.render(elem, True, (255, 255, 255)) for elem in ABOUT_ME]
        self.rules = [self.rules_font.render(elem, True, (255, 255, 255)) for elem in RULES]
        self.modes = [self.surface.render(elem, True, (255, 255, 255)) for elem in MODES]
        self.background = [(22, 171, 59), (7, 82, 65), (222, 134, 27), (199, 18, 18)]
        self.title = self.surface.render(NAME, True, (20, 116, 135))
        self.head = self.rules_font.render('Choose game mode', True, (255, 255, 255))
        self.back = self.back_font.render('Press enter to return to the menu', True, (115, 7, 7))
        self.current_ind = 0

    def start(self):
        running = True
        while running:
            for event in self.game.event.get():
                if event.type == self.game.QUIT:
                    running = False
                elif event.type == self.game.KEYDOWN:
                    if event.key == self.game.K_w or event.key == self.game.K_UP:
                        self._switch(-1)
                    if event.key == self.game.K_s or event.key == self.game.K_DOWN:
                        self._switch(1)
                    if event.key == self.game.K_RETURN:
                        if self.current_ind == 0:
                            self.select_mode(self.screen)
                        elif self.current_ind == 1:
                            self.screen.fill((0, 0, 0))
                            self._print_rules_and_about(self.screen, self.rules)
                        if self.current_ind == 2:
                            self.screen.fill((0, 0, 0))
                            self._print_rules_and_about(self.screen, self.about_me)
                        elif self.current_ind == 3:
                            self.game.quit()
                            exit()

            self.screen.fill(BLACK)
            self._menu()
            pygame.display.flip()

    def select_mode(self, surf):
        self.current_ind = 0
        while True:
            for event in self.game.event.get():
                if event.type == self.game.K_BACKSPACE:
                    break
                if event.type == self.game.KEYDOWN:
                    if event.key == self.game.K_w or event.key == self.game.K_UP:
                        self._switch(-1)
                    if event.key == self.game.K_s or event.key == self.game.K_DOWN:
                        self._switch(1)
                    if event.key == self.game.K_RETURN:
                        Game(MODES[self.current_ind]).start()

            self.screen.fill((0, 0, 0))
            head = self.head.get_rect()
            head.center = (HEIGHT // 2, WIDGHT // 10)
            self.game.draw.rect(surf, (0, 0, 0), head)
            surf.blit(self.head, head)
            for i, option in enumerate(self.modes):
                option_rect = option.get_rect()
                option_rect.center = (HEIGHT // 2, (WIDGHT // 3) + i * 75)
                if i == self.current_ind:
                    self.game.draw.rect(surf, self.background[i], option_rect)
                surf.blit(option, option_rect)
            pygame.display.flip()

    def _print_rules_and_about(self, surf, char):
        while True:
            for i, option in enumerate(char):
                option_rect = option.get_rect()
                option_rect.center = (HEIGHT // 2, (WIDGHT // 4) + i * 75)
                self.game.draw.rect(surf, (0, 0, 0), option_rect)
                surf.blit(option, option_rect)
            for event in self.game.event.get():
                if event.type == self.game.KEYDOWN:
                    if event.key == self.game.K_RETURN:
                        return
            back_menu = self.back.get_rect()
            back_menu.center = (HEIGHT // 2, WIDGHT - 100)
            self.game.draw.rect(surf, (0, 0, 0), back_menu)
            surf.blit(self.back, back_menu)
            pygame.display.flip()

    def _switch(self, direction):
        self.current_ind = max(0, min(self.current_ind + direction, len(self.options) - 1))

    def _menu(self):
        title = self.title.get_rect()
        title.center = (HEIGHT // 2, WIDGHT // 10)
        self.game.draw.rect(self.screen, BLACK, title)
        self.screen.blit(self.title, title)
        for i, option in enumerate(self.options):
            option_rect = option.get_rect()
            option_rect.center = (HEIGHT // 2, (WIDGHT // 3) + i * 75)
            if i == self.current_ind:
                self.game.draw.rect(self.screen, (96, 116, 120), option_rect)
            self.screen.blit(option, option_rect)


def main():
    Menu().start()


if __name__ == '__main__':
    main()
