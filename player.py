from _import import *
from scoreboard import Scoreboard
from round import Round
from button import Button
class Player(): 
    def __init__(self,scoreboard,round):
        self.name = ""
        self.rounds_played = 0
        self.total_score = 0
        self.scoreboard = scoreboard
        self.round = round
    
    def add_points(self, points):
        self.total_score += points
        self.scoreboard.update_score(self.name, self.total_score)
    
    def name_player(self, screen, font):
        input_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 50)
        color_inactive = (180, 180, 180)
        color_active = (255, 255, 255)
        color = color_inactive
        active = False
        text = ""
        done = False

        # Dodaj przycisk "Potwierdź"
        confirm_btn = Button(WIDTH // 2 - 75, HEIGHT // 2 + 75, 150, 40, "Potwierdź")
        confirm_btn.show()

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Aktywuj pole po kliknięciu
                    if input_box.collidepoint(event.pos):
                        active = True
                        color = color_active
                    else:
                        active = False
                        color = color_inactive
                    # Obsługa przycisku "Potwierdź"
                    if confirm_btn.is_clicked(event.pos):
                        if text:
                            done = True
                elif event.type == pygame.KEYDOWN and active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if len(text) < 15:  # limit znaków
                            text += event.unicode

            screen.fill((0, 0, 0))
            prompt = font.render("Podaj nazwe gracza: ", True, (255,255,255))
            screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 - 80))
            pygame.draw.rect(screen, color, input_box, 2)
            txt_surface = font.render(text, True, (255,255,255))
            screen.blit(txt_surface, (input_box.x+10, input_box.y+10))
            confirm_btn.draw(screen)
            pygame.display.flip()
        self.name = text
            