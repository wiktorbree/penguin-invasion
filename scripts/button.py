import pygame

SCALE = 2.0

class Button:
    def __init__(self, game, font, text, width, height, pos, elevation) -> None:
        self.game = game
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.org_y_pos = pos[1]
        self.done = False

        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#FFFFFF'

        self.bottom_rect = pygame.Rect(pos, (width, elevation))
        self.bottom_color = '#a1acbf'

        self.text_surf = font.render(text, False, '#393457')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def render(self):
        self.top_rect.y = self.org_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(self.game, self.bottom_color, self.bottom_rect, border_radius=7)
        pygame.draw.rect(self.game, self.top_color, self.top_rect, border_radius=7)
        self.game.blit(self.text_surf, self.text_rect)
        self.check_click()
        return self.done
    
    def check_click(self):
        mpos = pygame.mouse.get_pos()
        mpos = (mpos[0] / SCALE, mpos[1] / SCALE)
        if self.top_rect.collidepoint(mpos):
            self.top_color = '#c8e0e0'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed == True:
                    self.done = True
                    self.pressed = False
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = '#FFFFFF'