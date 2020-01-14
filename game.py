import pygame


class Game():
    def __init__(self):
        self.width = 1600
        self.height = 900
        self.window = pygame.display.set_mode((self.width, self.height))
        self.window_rect = self.window.get_rect()
        self.bg = pygame.Color("black")

        self.player_size = 100
        self.player_color = (255, 255, 255)
        self.player_rect = pygame.Rect(0, 0, self.player_size, self.player_size)
        self.player_rect.center = self.window_rect.center
        self.player_imgs = []
        self.animation_count = 0
        self.img = None

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pass
                    elif event.key == pygame.K_DOWN:
                        pass

                pos = pygame.mouse.get_pos()

            self.draw()

        pygame.quit()

    def draw(self):
        if self.animation_count >= len(self.player_imgs):
            self.animation_count = 0
        self.img = self.player_imgs[self.animation_count]
        self.window.blit(self.img, self.window_rect.center)
        # pygame.draw.rect(self.window, self.player_color, self.player_rect)
        pygame.display.update()
        self.animation_count += 1

    def rotate(self):
        pass

    def guess(self):
        pass

    def show_hint(self):
        pass

    def reset(self):
        pass


g = Game()
g.run()
