from _import import *
from dice import Dice
from button import Button
# Inicjalizacja pygame
pygame.init()

# Ustawienia okna

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yahtzee")
music = pygame.mixer.Sound('sound/muza.mp3')
music.set_volume(0.1)  # Ustaw głośność dźwięku
music.play()

# Font
font = pygame.font.Font(None, 36)





def handle_events(event, dices, roll, reroll):
    if event.type == pygame.QUIT:
        return False
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if roll.is_clicked(event.pos):
            for dice in dices:
                dice.start_roll(dices)
            roll.hide()
            reroll.show()
        elif reroll.is_clicked(event.pos):
            for dice in dices:
                dice.reroll(dices)
        else:
            for dice in dices:
                dice.toggle_selected(event.pos)
    return True

def update_dices(dices):
    for dice in dices:
        dice.update()

def draw_game(screen, dices, roll, reroll):
    screen.fill(BLACK)
    for dice in dices:
        dice.draw(screen)
    roll.draw(screen)
    reroll.draw(screen)
    y_offset = 10
    for i, dice in enumerate(dices):
        if not dice.is_rolling:
            result_text = font.render(f"Kostka {i+1}: {dice.current_dice}", True, WHITE)
            screen.blit(result_text, (10, y_offset))
            y_offset += 30
    pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    dices = Dice.add_dice()
    roll = Button(WIDTH // 2 - 100, HEIGHT - 120, 140, 50, "Rzuć kostką")
    reroll = Button(WIDTH // 2 - 100, HEIGHT - 120, 140, 50, "Ponownie")
    roll.show()
    reroll.hide()

    running = True
    while running:
        for event in pygame.event.get():
            running = handle_events(event, dices, roll, reroll)

        if all(not dice.is_rolling for dice in dices) and reroll.visible:
            reroll.show()

        update_dices(dices)
        draw_game(screen, dices, roll, reroll)
        clock.tick(60)

    pygame.quit()
    exit()

if __name__ == "__main__":
    main()
