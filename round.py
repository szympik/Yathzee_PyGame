from _import import *
from dice import Dice
from button import Button

class Round:
    def __init__(self, screen, current_turn=1, max_turns=1, max_rolls=3):
        self.screen = screen
        self.current_turn = current_turn
        self.max_turns = max_turns
        self.roll_count = 0
        self.max_rolls = max_rolls
        self.dices = Dice.add_dice()
        self.roll = Button(WIDTH // 2 - 100, HEIGHT - 120, 140, 50, "Rzuć kostką")
        self.reroll = Button(WIDTH // 2 - 100, HEIGHT - 120, 140, 50, "Ponownie")
        self.roll.show()
        self.reroll.hide()
        self.font = pygame.font.Font(None, 36)
        self.game_over = False
        self.background = pygame.image.load("img/dice_background.png")
        self.background = pygame.transform.scale(self.background, (1200, 800))
        self.game_over_image = pygame.image.load("img/game_over.png")
        self.game_over_image = pygame.transform.scale(self.game_over_image, (300, 100))
    def draw_empty_cup(self):
        cup_image = pygame.image.load("img/kubek_animacja/6.png")
        cup_image = pygame.transform.scale(cup_image, (400, 400))
        cup_x = WIDTH - 300
        cup_y = HEIGHT - 350
        self.screen.blit(cup_image, (cup_x, cup_y))

    def draw_full_cup(self):
        cup_image = pygame.image.load("img/kubek_animacja/1.png")
        cup_image = pygame.transform.scale(cup_image, (400, 400))
        cup_x = WIDTH - 300
        cup_y = HEIGHT - 350
        self.screen.blit(cup_image, (cup_x, cup_y))

    def draw_game_over(self, total_scores):
        self.screen.fill(BLACK)
        title_text = self.font.render("Koniec gry!", True, (255, 255, 255))
        self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
        image_rect = self.game_over_image.get_rect(center=(WIDTH // 2, 80))
        self.screen.blit(self.game_over_image, image_rect)
        # Sortowanie wyników malejąco po wyniku
        sorted_scores = sorted(total_scores, key=lambda x: x[1], reverse=True)

        medal_colors = [
            (255, 215, 0),  # złoto
            (192, 192, 192),  # srebro
            (205, 127, 50)  # brąz
        ]
        white = (255, 255, 255)

        start_y = 150
        line_height = 40

        last_score = None
        last_rank = 0

        for i, (player_name, score) in enumerate(sorted_scores, start=1):
            if score == last_score:
                rank = last_rank  # ten sam ranking co poprzedni gracz
            else:
                rank = i  # nowe miejsce

            last_score = score
            last_rank = rank

            # kolor medalu tylko dla miejsc 1-3 (tie rank)
            if rank <= 3:
                color = medal_colors[rank - 1]
            else:
                color = white

            text = self.font.render(f"{rank}. {player_name}: {score}", True, color)
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, start_y + (i - 1) * line_height))

        pygame.display.flip()

    def cup_animation(self):
        
      
        total_frames = 6
        images = {}

        for frame in range(1, total_frames + 1):
            img_path = f"img/kubek_animacja/{frame}.png"
            if os.path.exists(img_path):
                img = pygame.image.load(img_path)
                images[frame] = pygame.transform.scale(img, (400, 400))

        cup_x = WIDTH - 300
        cup_y = HEIGHT - 350

        current_frame = 1
        frame_counter = 0
        animation_speed = 2
        
        cup_sound = pygame.mixer.Sound("sound/shaking_dice.mp3")
        cup_sound.set_volume(0.1)
        cup_sound.play()

        clock = pygame.time.Clock()
        
        
        while current_frame <= total_frames:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            frame_counter += 1

            if frame_counter >= animation_speed:
                frame_counter = 0
                current_frame += 1

            if current_frame <= total_frames and current_frame in images:
                self.screen.blit(images[current_frame], (cup_x, cup_y))

            pygame.display.flip()
            clock.tick(30)

        self.draw_empty_cup()
        cup_sound.stop()

    def get_dices(self):
        return [dice.get_value() for dice in self.dices]

    def handle_events(self, event,scoreboard):
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.roll_count >= self.max_rolls:
                for dice in self.dices:
                    dice.toggle_selected(event.pos)
                return True

            if self.roll.is_clicked(event.pos):
                self.cup_animation()
                for dice in self.dices:
                    dice.start_roll(self.dices)
                self.roll.hide()
                self.reroll.show()
                return "roll"  # Zwróć informację o rzucie
                
            elif self.reroll.is_clicked(event.pos):
                self.hide_dices(scoreboard)
                self.cup_animation()
                for dice in self.dices:
                    dice.reroll(self.dices)
                return "reroll"  # Zwróć informację o powtórnym rzucie
                
            else:
                for dice in self.dices:
                    dice.toggle_selected(event.pos)
        return True

    def update_dices(self):
        for dice in self.dices:
            dice.update()

    def draw_turn_info(self):
        text = self.font.render(f"Runda: {self.current_turn} / {self.max_turns}   Rzuty: {self.roll_count} / {self.max_rolls}", True, (255, 255, 255))
        self.screen.blit(text, (50, 10))

    def draw_game(self, scoreboard, player_name=""):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (600, 0))
        scoreboard.draw(self.screen)

        for dice in self.dices:
            dice.draw(self.screen)

        self.roll.draw(self.screen)
        self.reroll.draw(self.screen)

        if self.roll_count == 0:
            self.draw_full_cup()
        else:
            self.draw_empty_cup()

        self.draw_turn_info()

        if player_name:
            name_text = self.font.render(f"Tura gracza: {player_name}", True, (255,255,255))
            self.screen.blit(name_text, (370, 10))

        pygame.display.flip()

    def increase_roll_count(self):
        self.roll_count += 1

    def next_turn(self):
        self.current_turn += 1
        self.roll_count = 0
        self.roll.show()
        self.reroll.hide()
        for dice in self.dices:
            dice.reset()
        
        if self.current_turn > self.max_turns:
            self.game_over = True
            
    def is_game_over(self):
        return self.game_over
        
    def update_roll_buttons(self):
        if self.roll.visible and self.roll_count >= self.max_rolls:
            self.roll.hide()
            self.reroll.show()


    def reset(self):
        self.roll_count = 0
        for dice in self.dices:
            dice.reset()
        self.roll.show()
        self.reroll.hide()
        self.draw_full_cup()

    def hide_dices(self,scoreboard):
        for dice in self.dices:
            if dice.selected==False:
                dice.current_pos = (-100, -100)
        self.draw_game(scoreboard)
        pygame.display.flip()