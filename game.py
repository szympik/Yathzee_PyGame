from _import import *
from dice import Dice
from button import Button
from scoreboard import Scoreboard

pygame.init()

# Ustawienia okna
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yahtzee")

music = pygame.mixer.Sound('sound/muza.mp3')
music.set_volume(0.0)
music.play()

font = pygame.font.Font(None, 36)
def draw_empty_cup(screen):
    cup_image = pygame.image.load("img/kubek_animacja/6.png")
    cup_image = pygame.transform.scale(cup_image, (400, 400))
    cup_x = WIDTH - 300
    cup_y = HEIGHT - 350
    screen.blit(cup_image, (cup_x, cup_y))
def draw_full_cup(screen):
    cup_image = pygame.image.load("img/kubek_animacja/1.png")
    cup_image = pygame.transform.scale(cup_image, (400, 400))
    cup_x = WIDTH - 300
    cup_y = HEIGHT - 350
    screen.blit(cup_image, (cup_x, cup_y))

def draw_game_over(screen, total_score, font):
    screen.fill(BLACK)
    text1 = font.render("Koniec gry!", True, (255, 255, 255))
    text2 = font.render(f"Twój wynik: {total_score}", True, (255, 255, 255))
    screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 2 - 40))
    screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2 + 10))
    pygame.display.flip()

def cup_animation(screen):
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
            screen.blit(images[current_frame], (cup_x, cup_y))

        pygame.display.flip()
        clock.tick(30)

    draw_empty_cup(screen)
    cup_sound.stop()

def get_dices(dices):
    return [dice.get_value() for dice in dices]


def handle_events(event, dices, roll, reroll, roll_count, max_rolls):
    if event.type == pygame.QUIT:
        return False
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if roll_count >= max_rolls:
            for dice in dices:
                dice.toggle_selected(event.pos)
            return True

        if roll.is_clicked(event.pos):
            cup_animation(screen)
            for dice in dices:
                dice.start_roll(dices)
            roll.hide()
            reroll.show()
            return "roll"  # Zwróć informację o rzucie
            
        elif reroll.is_clicked(event.pos):
            cup_animation(screen)
            for dice in dices:
                dice.reroll(dices)
            return "reroll"  # Zwróć informację o powtórnym rzucie
            
        else:
            for dice in dices:
                dice.toggle_selected(event.pos)
    return True


def update_dices(dices):
    for dice in dices:
        dice.update()

background = pygame.image.load("img/dice_background.png")
background = pygame.transform.scale(background, (1200, 800))

def draw_turn_info(screen, current_turn, max_turns, roll_count, max_rolls, font):
    text = font.render(f"Runda: {current_turn} / {max_turns}   Rzuty: {roll_count} / {max_rolls}", True, (255, 255, 255))
    screen.blit(text, (50, 10))

def draw_game(screen, dices, roll, reroll, scoreboard, current_turn, max_turns, roll_count, max_rolls, font):
    screen.fill(BLACK)
    screen.blit(background, (600, 0))
    scoreboard.draw(screen)
    

    for dice in dices:
        dice.draw(screen)

    roll.draw(screen)
    reroll.draw(screen)
    
    if roll_count == 0:
        draw_full_cup(screen)
    else:
        draw_empty_cup(screen)
        
    draw_turn_info(screen, current_turn, max_turns, roll_count, max_rolls, font)

    pygame.display.flip()


def main():
    clock = pygame.time.Clock()
    dices = Dice.add_dice()
    roll = Button(WIDTH // 2 - 100, HEIGHT - 120, 140, 50, "Rzuć kostką")
    reroll = Button(WIDTH // 2 - 100, HEIGHT - 120, 140, 50, "Ponownie")
    roll.show()
    reroll.hide()

    current_turn = 1
    max_turns = 3  # lub 13
    roll_count = 0
    max_rolls = 3
    scoreboard = Scoreboard(x=50, y=50)
    font = pygame.font.Font(None, 36)

    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                if roll_count > 0 and scoreboard.handle_click(event.pos, get_dices(dices)):
                    current_turn += 1
                    roll_count = 0
                    roll.show()
                    reroll.hide()
                    for dice in dices:
                        dice.reset()
                    
                    if current_turn > max_turns:
                        game_over = True
                else:
                    event_result = handle_events(event, dices, roll, reroll, roll_count, max_rolls)
                    if event_result == "roll":
                        roll_count += 1
                    elif event_result == "reroll":
                        roll_count += 1
                    elif event_result == False:
                        running = False

        if not game_over:
            if roll.visible and roll_count >= max_rolls:
                roll.hide()
                reroll.show()

            update_dices(dices)
            draw_game(screen, dices, roll, reroll, scoreboard, current_turn, max_turns, roll_count, max_rolls, font)


        else:
            total = scoreboard.total_score()
            draw_game_over(screen, total, font)

        clock.tick(60)

    pygame.quit()
    exit()

if __name__ == "__main__":
    main()
