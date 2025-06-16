from _import import *
from scoreboard import Scoreboard
from round import Round
from button import Button

class Player(): 
    def __init__(self,scoreboard,round,number):
        """Inicjalizuje gracza z własnym scoreboardem i rundą."""
        self.name = ""
        self.rounds_played = 0
        self.total_score = 0
        self.scoreboard = scoreboard
        self.round = round
        self.number = number  
    
    def add_points(self, points):
        """Dodaje punkty do całkowitego wyniku gracza i aktualizuje scoreboard."""
        self.total_score += points
        self.scoreboard.update_score(self.name, self.total_score)
    
    def name_player(self, screen, font):
        """Wyświetla okno do wpisania imienia gracza i zapisuje je."""
        input_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 50)
        color_inactive = (180, 180, 180)
        color_active = (255, 255, 255)
        color = color_inactive
        active = False
        text = ""
        done = False


        confirm_btn = Button(WIDTH // 2 - 120, HEIGHT // 2 + 70, 240, 65, "Potwierdź")
        confirm_btn.show()

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = True
                        color = color_active
                    else:
                        active = False
                        color = color_inactive
                    if confirm_btn.is_clicked(event.pos):
                        if text:
                            done = True
                elif event.type == pygame.KEYDOWN and active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if len(text) < 15:
                            text += event.unicode

            screen.fill(DARK_GREEN)
            if self.number == 0:
                prompt = font.render(f"Podaj nazwe gracza: ", True, GOLD)
            else:     
                prompt = font.render(f"Podaj nazwe gracza {self.number+1}: ", True, GOLD)
            screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 - 80))
            pygame.draw.rect(screen, YELLOW, input_box, 2)
            txt_surface = font.render(text, True, GOLD)
            screen.blit(txt_surface, (input_box.x+10, input_box.y+2))
            confirm_btn.draw(screen)
            pygame.display.flip()
        self.name = text
