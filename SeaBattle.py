import pygame
from config import RULES, ABOUT_ME, MODES, MENU, POSITIONS, HEIGHT, WIDGHT, NAME, WHITE, BLACK, SHIPS, HELP_MESSAGE_1, HELP_MESSAGE_2
from time import sleep
import random


class Game:
    def __init__(self, mode) -> None:
        self.turn = True
        self.game = pygame
        self.game.init()
        self.screen = pygame.display.set_mode((HEIGHT, WIDGHT))#, flags=pygame.NOFRAME)
        self.user_fild = self.game.draw.rect(self.screen, (71, 76, 112), (15, 15, 260, 260))
        self.surface = self.game.font.SysFont('arial', 18)
        self.options = self.game.font.SysFont('arial', 30)
        self.mode = mode
        self.letters = [self.surface.render(elem, True,
                                            (255, 255, 255)) for elem in 'ABCDEFGHIJ']
        self.nums = [self.surface.render(str(elem), True,
                                         (255, 255, 255)) for elem in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
        self.info = self.surface.render('Incorrect Position', True, (115, 7, 7))
        self.choose_optns = [self.options.render(elem, True, (255, 255, 255)) for elem in POSITIONS]
        self.first_help_message = self.surface.render(HELP_MESSAGE_1, True, WHITE)
        self.first_help_mes_on_field = self.surface.render(HELP_MESSAGE_2, True, WHITE)
        self.ships = SHIPS
        self.field_size = 10
        self.block_size = 24
        self.left_marg = 40
        self.upper_marg = 50
        self.user_size = 13
        self.opt_ind = 0
        self.menu_ind = 0
        self.player_mode = 0
        self.font_size = int(self.block_size / 1.5)
        self.font = self.game.font.SysFont('notosize', self.font_size)
        self.ships_on_fiend_rect = []
        self.bot_ships_on_field_rect = []
        self.ships_coodrinate = []
        self.bot_ships_coodrinate = []

    def start(self):
        self.screen.fill(BLACK)
        self.player_mode = self.choose_positions()
        self.screen.fill(BLACK)
        if self.player_mode == 0:
            self.generate_ship(True)
            self.generate_ship(False)
            print('lets go')
            self.start_match()
        else:
            self.generate_ship(False)
            self.draw_field()
            while True:
                for event in pygame.event.get():
                    if event.type == self.game.KEYDOWN:
                        if event.key == self.game.K_BACKSPACE:
                            exit()
                        if event.key == self.game.K_w or event.key == self.game.K_UP:
                            self.menu_ind = self._switch_ind(self.menu_ind, -1, self.ships)
                        if event.key == self.game.K_s or event.key == self.game.K_DOWN:
                            self.menu_ind = self._switch_ind(self.menu_ind, 1, self.ships)
                        if event.key == self.game.K_RETURN:
                            self.screen.fill(BLACK, help_message)
                            if self.draw_ship(list(self.ships.keys())[self.menu_ind]):
                                self.ships[list(self.ships.keys())[self.menu_ind]] -=  1

                if len(self.ships_coodrinate) == 10:
                    print('lets go')
                    self.start_match()
                else:
                    help_message = self.first_help_message.get_rect()
                    help_message.center = (HEIGHT // 2, WIDGHT - 100)
                    self.game.draw.rect(self.screen, (0, 0, 0), help_message)
                    self.screen.blit(self.first_help_message, help_message)
                    self.game.display.update()
                    self.select_ship()
                    self.game.display.update()

    def start_match(self):
        print('im here')
        exit()

    def choose_positions(self):
        running = True
        self.screen.fill(BLACK)
        self.game.display.update()
        while running:
            for event in self.game.event.get():
                if event.type == self.game.KEYDOWN:
                    if event.key == self.game.K_BACKSPACE:
                        exit()
                    if event.key == self.game.K_w or event.key == self.game.K_UP:
                        self.opt_ind = self._switch_ind(self.opt_ind, -1, self.choose_optns)
                    if event.key == self.game.K_s or event.key == self.game.K_DOWN:
                        self.opt_ind = self._switch_ind(self.opt_ind, 1, self.choose_optns)
                    if event.key == self.game.K_RETURN:
                        return self.opt_ind

            self.screen.fill(BLACK)
            for i, option in enumerate(self.choose_optns):
                opt_rect = option.get_rect()
                opt_rect.center = (HEIGHT // 2, (WIDGHT // 2.5) + i * 75)
                if i == self.opt_ind:
                    self.game.draw.rect(self.screen, (96, 116, 120), opt_rect)
                self.screen.blit(option, opt_rect)
            self.game.display.flip()

    def draw_ship(self, ship):
        self.turn = True
        len_ship = ship.split('-')[0]
        x = self.left_marg
        y = self.upper_marg + 12 * self.block_size
        h = self.block_size * int(len_ship) + 1
        w = self.block_size + 1
        while True:
            start_pos = self.game.Rect(x, y, h, w)
            if self.turn:
                cur_pos = ((x // self.block_size, (y  // self.block_size) - self.user_size),
                           ((x // self.block_size) + int(len_ship) - 1, (y  // self.block_size) - self.user_size))
            else:
                cur_pos = ((x // self.block_size, (y  // self.block_size) - self.user_size),
                           ((x // self.block_size), (y  // self.block_size) - self.user_size + int(len_ship) - 1))
            for event in self.game.event.get():
                if event.type == self.game.KEYDOWN:
                    if event.key == self.game.K_BACKSPACE:
                        self.draw_field()
                        return False
                    if event.key == self.game.K_LEFT or event.key == self.game.K_a:
                        if x <= self.left_marg:
                            pass
                        else:
                            x -= self.block_size
                    if event.key == self.game.K_RIGHT or event.key == self.game.K_d:
                        if self.turn:
                            if x + (int(len_ship) - 1) * self.block_size >= 256:
                                pass
                            else:
                                x += self.block_size
                        else:
                            if x >= 256:
                                pass
                            else:
                                x += self.block_size
                    if event.key == self.game.K_UP or event.key == self.game.K_w:
                        if y <= 338:
                            pass
                        else:
                            y -= self.block_size
                    if event.key == self.game.K_DOWN or event.key == self.game.K_s:
                        if self.turn:
                            if y >= 554:
                                pass
                            else:
                                y += self.block_size
                        else:
                            if y + (int(len_ship) * self.block_size) - 1 >= 554:
                                pass
                            else:
                                y += self.block_size
                    if event.key == self.game.K_r:
                        if self.turn:
                            h = self.block_size + 1
                            w = self.block_size * int(len_ship) + 1
                            if y + (int(len_ship) * self.block_size) - 1 >= 554:
                                y = y - (int(len_ship) * self.block_size)
                            if x + (int(len_ship) - 1) * self.block_size >= 256:
                                x = x - (int(len_ship) - 1) * self.block_size
                            self.turn = False
                        else:
                            h = self.block_size * int(len_ship) + 1
                            w = self.block_size + 1
                            if y + (int(len_ship) * self.block_size)- 1 >= 554:
                                y = y - (int(len_ship) * self.block_size)
                            if x + (int(len_ship) - 1) * self.block_size >= 256:
                                x = x - (int(len_ship) - 1) * self.block_size 
                            self.turn = True
                        continue
                    if event.key == self.game.K_RETURN:
                        # coordinate
                        if self._check_position(cur_pos, self.ships_coodrinate):
                            self.ships_on_fiend_rect.append(start_pos)
                            self.ships_coodrinate.append(cur_pos)
                            self.draw_field()
                            self._draw_ships()
                            self.screen.fill(BLACK, help_mesg)
                            return True
                        else:
                            self.screen.fill(BLACK, help_mesg)
                            info = self.info.get_rect()
                            info.center = (HEIGHT // 2, WIDGHT - 100)
                            self.game.draw.rect(self.screen, (0, 0, 0), info)
                            self.screen.blit(self.info, info)
                            self.game.display.update()
                            sleep(1)
                            self.screen.fill(BLACK, info)
                            self.draw_field()
                            self._draw_ships()
                            self.screen.fill(BLACK, help_mesg)
                            self.turn = True

            help_mesg = self.first_help_mes_on_field.get_rect()
            help_mesg.center = (HEIGHT // 1.8, WIDGHT - 100)
            self.game.draw.rect(self.screen, (0, 0, 0), help_mesg)
            self.screen.blit(self.first_help_mes_on_field, help_mesg)
            self.game.display.update()
            self.draw_field()
            if self._check_position(cur_pos, self.ships_coodrinate):
                self.game.draw.rect(self.screen, (0, 255, 55), self.game.Rect(start_pos), 1)
                self.game.display.update()
            else:
                self.game.draw.rect(self.screen, (255, 0, 0), self.game.Rect(start_pos), 1)
                self.game.display.update()

    def generate_ship(self, is_user):
        x = [i for i in range(1, 11)]
        y = [i for i in range(1, 11)]
        for k, v in self.ships.items():
            for i in range(v):
                size = k.split('-')[0]
                coord_x = random.choice(x)
                coord_y = random.choice(y)
                reverse = random.choice([1, 0])
                while True:
                    res = (self.draw_bot_ship((coord_x, coord_y), int(size), reverse, is_user))
                    if res:
                        cur_x, cur_y = res
                        x[:].remove(cur_x)
                        y[:].remove(cur_y)
                        break
                    else:
                        coord_x = random.choice(x)
                        coord_y = random.choice(y)
        if is_user:
            for i in range(len(self.ships_on_fiend_rect)):
                self.ships_on_fiend_rect[i][0] += 1
                self.ships_on_fiend_rect[i][1] += 1
                self.ships_on_fiend_rect[i][2] -= 2
                self.ships_on_fiend_rect[i][3] -= 2
                self.game.draw.rect(self.screen, (105, 128, 255), self.ships_on_fiend_rect[i])
                self.game.display.update()
                sleep(0.1)
        else:
            for i in range(len(self.bot_ships_on_field_rect)):
                self.bot_ships_on_field_rect[i][0] += 1
                self.bot_ships_on_field_rect[i][1] += 1
                self.bot_ships_on_field_rect[i][2] -= 2
                self.bot_ships_on_field_rect[i][3] -= 2
                self.game.draw.rect(self.screen, (105, 128, 255), self.bot_ships_on_field_rect[i])
                self.game.display.update()
                sleep(0.1)

    def draw_bot_ship(self, coordinate, size, is_reverse, is_user):
        self.draw_field()
        self.game.display.update()
        x_coord = coordinate[0]
        y_coord = coordinate[1]
        if is_user:
            x_max = self.left_marg + self.block_size * (self.field_size - 1)
            y_max = 554

            if is_reverse:
                x = self.left_marg + (x_coord * self.block_size) - self.block_size
                y = self.upper_marg + (self.user_size - 2) * self.block_size + y_coord * self.block_size
                h = self.block_size + 1
                w = self.block_size * (size) + 1

            else:
                x = self.left_marg + (x_coord * self.block_size) - self.block_size
                y = self.upper_marg + (self.user_size - 2) * self.block_size + y_coord * self.block_size
                h = self.block_size * (size) + 1
                w = self.block_size + 1

            if y + self.block_size * (size - 1) > y_max:
                y -= self.block_size * (size - 1)

            if x + self.block_size * (size - 1) > x_max:
                x -= self.block_size * (size - 1)

            cur_pos = self.game.Rect(x, y, w, h)
            if is_reverse:
                ship_coord = ((x // self.block_size, (y  // self.block_size - 1) - (self.user_size - 1)),
                                            ((x // self.block_size) + size - 1, (y  // self.block_size - 1) - (self.user_size - 1)))
            else:
                ship_coord = ((x // self.block_size, (y  // self.block_size - 1) - (self.user_size - 1)),
                                            ((x // self.block_size), (y  // self.block_size - 1) + size - 1- (self.user_size - 1)))
            if self._check_position(ship_coord, self.ships_coodrinate):
                self.ships_coodrinate.append(ship_coord)
                self.ships_on_fiend_rect.append(cur_pos)
                x, y = (x // self.block_size, (y  // self.block_size - 1) - (self.user_size - 1))
                return (x, y)
            return False
        else:
            x_max = self.left_marg + self.block_size * (self.field_size - 1)
            y_max = self.upper_marg + self.block_size * (self.field_size - 1)

            if is_reverse:
                x = self.left_marg + (x_coord * self.block_size) - self.block_size
                y = self.upper_marg + (y_coord * self.block_size) - self.block_size
                h = self.block_size + 1
                w = self.block_size * (size) + 1

            else:
                x = self.left_marg + (x_coord * self.block_size) - self.block_size
                y = self.upper_marg + (y_coord * self.block_size) - self.block_size
                h = self.block_size * (size) + 1
                w = self.block_size + 1

            if y + self.block_size * (size - 1) > y_max:
                y -= self.block_size * (size - 1)

            if x + self.block_size * (size - 1) > x_max:
                x -= self.block_size * (size - 1)

            cur_pos = self.game.Rect(x, y, w, h)
            if is_reverse:
                ship_coord = ((x // self.block_size, (y  // self.block_size - 1)),
                                            ((x // self.block_size) + size - 1, (y  // self.block_size - 1)))
            else:
                ship_coord = ((x // self.block_size, (y  // self.block_size - 1)),
                                            ((x // self.block_size), (y  // self.block_size - 1) + size - 1))
            if self._check_position(ship_coord, self.bot_ships_coodrinate):
                self.bot_ships_coodrinate.append(ship_coord)
                self.bot_ships_on_field_rect.append(cur_pos)
                x, y = (x // self.block_size, (y  // self.block_size - 1))
                return (x, y)
            return False

    def select_ship(self):
        self.game.draw.rect(self.screen, BLACK, (600, 300, 800, 800))
        for i, ship in enumerate(list(self.ships.keys())):
            count_ships = self.ships[ship]
            if count_ships > 0:
                ship = self.surface.render(f'{count_ships}x {ship}', True, WHITE)
            else:
                self.ships.pop(ship)
                continue
            ship_rect = ship.get_rect()
            ship_rect.center = (700, 330 + i * 25)
            if i == self.menu_ind:
                self.game.draw.rect(self.screen, (96, 116, 120), ship_rect)
            self.screen.blit(ship, ship_rect)

    def _check_position(self, ship_coord, all_ships):
        for elem in all_ships:
            for q in range(len(ship_coord)):
                x, y = ship_coord[q][0], ship_coord[q][1]
                if (x, y + 1) == elem[0] or (x, y + 1) == elem[1]:
                    return False
                if (x, y - 1) == elem[0] or (x, y - 1) == elem[1]:
                    return False
                if (x + 1, y) == elem[0] or (x + 1, y) == elem[1]:
                    return False
                if (x - 1, y) == elem[0] or (x - 1, y) == elem[1]:
                    return False
                if (x + 1, y + 1) == elem[0] or (x + 1, y + 1) == elem[1]:
                    return False
                if (x + 1, y - 1) == elem[0] or (x + 1, y - 1) == elem[1]:
                    return False
                if (x - 1, y + 1) == elem[0] or (x - 1, y + 1) == elem[1]:
                    return False
                if (x - 1, y - 1) == elem[0] or (x - 1, y - 1) == elem[1]:
                    return False
                if (x, y) == elem[0] or (x, y) == elem[1]:
                    return False

        return True

    def draw_field(self):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        title = self.font.render(self.mode, 1, WHITE)
        for y in range(11):
            for x in range(11):
                # first field
                self.game.draw.line(self.screen, WHITE, (self.left_marg,self.upper_marg + y * self.block_size),
                                    (self.left_marg + self.field_size * self.block_size, self.upper_marg + y * self.block_size), 1)
                self.game.draw.line(self.screen, WHITE, (self.left_marg + x * self.block_size,self.upper_marg),
                                    (self.left_marg + x * self.block_size,self.upper_marg + 10 * self.block_size), 1)
                # second field
                self.game.draw.line(self.screen, WHITE, (self.left_marg,(self.upper_marg + y * self.block_size) + 12 * self.block_size),
                                    (self.left_marg + self.field_size * self.block_size, (self.upper_marg + y * self.block_size)+ 12 * self.block_size), 1)
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
                self.screen.blit(char, (self.left_marg + y *self.block_size + (self.block_size // 2 - char_widht // 2), (self.upper_marg + self.field_size * self.block_size) + 5))
                # second field
                self.screen.blit(num, (self.left_marg - (self.block_size//2 + num_widht // 2), (self.upper_marg + y * self.block_size + (self.block_size // 2 - num_height // 2) + 12 * self.block_size)))
                self.screen.blit(char, (self.left_marg + y *self.block_size + (self.block_size // 2 - char_widht // 2), ((self.upper_marg + self.field_size * self.block_size) + 5) + 12 * self.block_size))
        title = self.surface.render(f'MODE : {self.mode}', 1, WHITE)
        head = title.get_rect()
        head.center = (HEIGHT // 2, WIDGHT // self.field_size)
        self.screen.blit(title, head)

    def _draw_ships(self):
        if self.ships_on_fiend_rect:
            for elem in self.ships_on_fiend_rect:
                elem[0] += 1
                elem[1] += 1
                elem[2] -= 2
                elem[3] -= 2
                self.game.draw.rect(self.screen, (105, 128, 255), elem)

    def _switch_ind(self, cur_ind, num, lst):
        cur_ind = max(0, min(cur_ind + num, len(lst) - 1))
        return cur_ind


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
