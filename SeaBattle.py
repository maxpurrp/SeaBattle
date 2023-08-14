import pygame
from config import RULES, ABOUT_ME, MODES, MENU, HEIGHT, WIDGHT, NAME

class Game:
    def __init__(self) -> None:
        self.game = pygame
        self.game.init()
        self.screen = pygame.display.set_mode((HEIGHT, WIDGHT), flags=pygame.NOFRAME)
        self.user_fild = self.game.draw.rect(self.screen, (71, 76, 112), (15, 15, 260, 260))
        self.surface = self.game.font.SysFont('arial', 15)
        self.letters = [self.surface.render(elem, True, (255, 255, 255)) for elem in 'ABCDEFGHIJ']
        self.nums = [self.surface.render(str(elem), True, (255, 255, 255)) for elem in [1,2,3,4,5,6,7,8,9,10]]
        self.widght = self.height = 14
        self.magrin = 10

    def start(self, mode):
        limiter_letter = 0
        limiter_nums = 0
        print(mode)
        self.screen.fill((0, 0, 0))
        self.game.draw.rect(self.screen, (71, 76, 112), (20, 25, 290, 260), 2)
        self.game.draw.rect(self.screen, (71, 76, 112), (20, 330, 290, 260), 2)
        while True:
            for event in pygame.event.get():
                if event.type == self.game.KEYDOWN:
                    if event.key == self.game.K_BACKSPACE:
                        exit()
            for col in range(10):
                for row in range(10):
                    x = col * self.widght + (col + 1) * self.magrin
                    y = row * self.height + (row + 1) * self.magrin
                    # x = 24 ->
                    # y = 24  ^
                    self.game.draw.rect(self.screen, (120, 18, 18), (x + 45, y + 35, self.widght, self.height), 2)
                    self.game.draw.rect(self.screen, (14, 21, 66), (x + 45, y + 340, self.widght, self.height), 2)
                    if limiter_letter != 10:
                        self.screen.blit(self.letters[row], (x + 20, y + 30))
                        self.screen.blit(self.letters[row], (x + 20, y + 335))
                        limiter_letter += 1
                if limiter_nums != 10:
                    self.screen.blit(self.nums[col], (x + 45, 25))
                    self.screen.blit(self.nums[col], (x + 45, 330))


            self.game.display.update()


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
            self.screen.fill((0, 0, 0))
            self._menu(self.screen)
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
                        Game().start(MODES[self.current_ind])

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

    def _menu(self, surf):
        title = self.title.get_rect()
        title.center = (HEIGHT // 2, WIDGHT // 10)
        self.game.draw.rect(surf, (0, 0, 0), title)
        surf.blit(self.title, title)
        for i, option in enumerate(self.options):
            option_rect = option.get_rect()
            option_rect.center = (HEIGHT // 2, (WIDGHT // 3) + i * 75)
            if i == self.current_ind:
                self.game.draw.rect(surf, (96, 116, 120), option_rect)
            surf.blit(option, option_rect)


def main():
    cur = Menu()
    cur.start()


if __name__ == '__main__':
    main()
