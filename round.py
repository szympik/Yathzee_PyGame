from _import import *
from dice import Dice
from button import Button

class Round:
    def __init__(self, screen, current_turn=1, max_turns=3, max_rolls=3):
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

    def draw_game_over(self, total_score):
        self.screen.fill(BLACK)
        text1 = self.font.render("Koniec gry!", True, (255, 255, 255))
        text2 = self.font.render(f"Twój wynik: {total_score}", True, (255, 255, 255))
        self.screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 2 - 40))
        self.screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2 + 10))
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

    def handle_events(self, event):
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

    def draw_game(self, scoreboard):
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