import pygame


class Slider:
    def __init__(self, game, x, y, length=200, width=2, color="white", slider_scale=1, value=0):
        self.game = game
        self.pos = (x, y)
        self.length = length
        self.width = width
        self.slider_size = (10 * slider_scale, 15 * slider_scale)
        self.bar = pygame.Surface((length, width))
        self.bar.fill(color)
        self.slider = pygame.Surface(self.slider_size)
        self.slider.fill(color)
        self.value = value
        self.grabbed = False

    def rect(self):
        return pygame.Rect(
            self.pos[0] + self.value * self.length - self.slider_size[0] / 2,
            self.pos[1] + (self.width / 2) - self.slider_size[1] / 2,
            self.slider_size[0],
            self.slider_size[1]
        )

    def update(self, mouse_just_clicked):
        if not pygame.mouse.get_pressed()[0]:
            self.grabbed = False

        mouse_pos = pygame.mouse.get_pos()
        if (mouse_just_clicked and self.rect().collidepoint(mouse_pos)) or self.grabbed:
            self.grabbed = True
            self.value = (mouse_pos[0] - self.pos[0]) / self.length
            if self.value < 0:
                self.value = 0
            if self.value > 1:
                self.value = 1

    def render(self):
        self.game.screen.blit(self.bar, (self.pos[0], self.pos[1]))
        self.game.screen.blit(self.slider, (self.pos[0] + self.value * self.length - self.slider_size[0] / 2,
                              self.pos[1] + (self.width / 2) - self.slider_size[1] / 2))
