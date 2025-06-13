from _import import *
from scoreboard import Scoreboard
from round import Round

pygame.init()

# Ustawienia okna
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yahtzee")

music = pygame.mixer.Sound('sound/muza.mp3')
music.set_volume(0.0)
music.play()

font = pygame.font.Font(None, 36)
    
def main():
    clock = pygame.time.Clock()
    scoreboard = Scoreboard(x=50, y=50)
    game_round = Round(screen)
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif not game_round.is_game_over() and event.type == pygame.MOUSEBUTTONDOWN:
                if game_round.roll_count > 0 and scoreboard.handle_click(event.pos, game_round.get_dices()):
                    game_round.next_turn()
                else:
                    event_result = game_round.handle_events(event,scoreboard)
                    if event_result == "roll":
                        game_round.increase_roll_count()
                    elif event_result == "reroll":
                        game_round.increase_roll_count()
                    elif event_result == False:
                        running = False

        if not game_round.is_game_over():
            game_round.update_roll_buttons()
            game_round.update_dices()
            game_round.draw_game(scoreboard)
        else:
            total = scoreboard.total_score()
            game_round.draw_game_over(total)

        clock.tick(60)

    pygame.quit()
    exit()

if __name__ == "__main__":
    main()
