from _import import *
from scoreboard import Scoreboard
from round import Round
from button import Button
from player import Player

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yahtzee")

music = pygame.mixer.Sound('sound/muza.mp3')
music.set_volume(0.0)
music.play()

font = pygame.font.Font(None, 36)

def main_menu():
    num_players = 2
    min_players = 1
    max_players = 6
    menu_running = True

    # Przyciski strzałek
    left_btn = Button(WIDTH // 2 - 250, HEIGHT // 2 - 25, 60, 50, "<")
    right_btn = Button(WIDTH // 2 + 190, HEIGHT // 2 - 25, 60, 50, ">")
    start_btn = Button(WIDTH // 2 - 50, HEIGHT // 2 + 80, 100, 50, "START")
    left_btn.show()
    right_btn.show()
    start_btn.show()

    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if left_btn.is_clicked(event.pos):
                    if num_players > min_players:
                        num_players -= 1
                elif right_btn.is_clicked(event.pos):
                    if num_players < max_players:
                        num_players += 1
                elif start_btn.is_clicked(event.pos):
                    menu_running = False
                    return num_players

                    

        screen.fill((0, 0, 0))
        title_text = font.render("Yahtzee", True, (255, 255, 255))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 120))

        left_btn.draw(screen)
        right_btn.draw(screen)
        start_btn.draw(screen)


        players_text = font.render(f"Liczba graczy: {num_players}", True, (255,255,255))
        screen.blit(players_text, (WIDTH // 2 - players_text.get_width() // 2, HEIGHT // 2 - players_text.get_height() // 2))

        pygame.display.flip()
       
def add_players(num_players):
    players = []
    for i in range(num_players):
        new_scoreboard = Scoreboard()
        new_round = Round(screen)  # TYLKO screen, bez scoreboard
        new_player = Player(new_scoreboard, new_round)
        new_player.name_player(screen, font)
        players.append(new_player)
    return players

    
def main():
    clock = pygame.time.Clock()
    players = add_players(main_menu())

    current_player_index = 0
    running = True

    while running:
        current_player = players[current_player_index]
        scoreboard = current_player.scoreboard
        game_round = current_player.round

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif not game_round.is_game_over() and event.type == pygame.MOUSEBUTTONDOWN:
                if game_round.roll_count > 0 and scoreboard.handle_click(event.pos, game_round.get_dices()):
                    current_player_index = (current_player_index + 1) % len(players)
                    game_round.next_turn()
                else:
                    event_result = game_round.handle_events(event, scoreboard)
                    if event_result == "roll":
                        game_round.increase_roll_count()
                    elif event_result == "reroll":
                        game_round.increase_roll_count()
                    elif event_result == False:
                        running = False


        if all(player.round.is_game_over() for player in players):
            total_scores = [(player.name, player.scoreboard.total_score()) for player in players]

            game_round.draw_game_over(total_scores)
            pygame.time.delay(5000)
            running = False
        else:
            if not game_round.is_game_over():
                game_round.update_roll_buttons()
                game_round.update_dices()
                game_round.draw_game(scoreboard, current_player.name)

            else:
                current_player_index = (current_player_index + 1) % len(players)

        clock.tick(60)

    pygame.quit()
    exit()



if __name__ == "__main__":
    
    main()
