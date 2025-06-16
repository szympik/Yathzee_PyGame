from _import import *

class Button:
    def __init__(self, x, y, width, height, text, image_path="img/button.png"):
        """Inicjalizuje przycisk z pozycją, rozmiarem, tekstem i opcjonalną grafiką."""
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font("fonts/font_bold.ttf", 36)
        self.image = pygame.image.load(image_path)
        self.visible = False

    def draw(self, surface):
        """Rysuje przycisk na podanej powierzchni jeśli jest widoczny."""
        if self.visible:
            pygame.draw.rect(surface, TRANSPARENT, self.rect, 2)
            self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
            surface.blit(self.image, self.rect.topleft)
            
            text_surface = self.font.render(self.text, True, YELLOW)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        """Zwraca True jeśli przycisk jest widoczny i kliknięty."""
        return self.visible and self.rect.collidepoint(pos)

    def show(self):
        """Ustawia przycisk jako widoczny."""
        self.visible = True

    def hide(self):
        """Ukrywa przycisk."""
        self.visible = False
