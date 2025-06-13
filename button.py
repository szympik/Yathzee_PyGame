from _import import *
 
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font("fonts/font.ttf", 36)
        self.visible = False

    def draw(self, surface):
        if self.visible:
            pygame.draw.rect(surface, GRAY, self.rect)
            pygame.draw.rect(surface, WHITE, self.rect, 2)
            text_surface = self.font.render(self.text, True, BLACK)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.visible and self.rect.collidepoint(pos)

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False
