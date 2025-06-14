from _import import *
from scoreboard import Scoreboard
from round import Round
from button import Button
from player import Player

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yahtzee")

music = pygame.mixer.Sound('sound/jazz.mp3')
music.set_volume(0.0)
music.play()

font = pygame.font.Font("fonts/font.ttf", 36)
timer_font = pygame.font.Font("fonts/font.ttf", 30)
def main_menu():
    num_players = 1
    min_players = 1
    max_players = 6
    menu_running = True

    # Przyciski strzałek
    left_btn = Button(WIDTH // 2 - 250, HEIGHT // 2 - 25, 60, 40, "", "img/left_arrow.png")
    right_btn = Button(WIDTH // 2 + 190, HEIGHT // 2 - 25, 60, 40, "", "img/right_arrow.png")
    start_btn = Button(WIDTH // 2 - 100, HEIGHT // 2 + 65, 200, 70, "Start")
    left_btn.show()
    right_btn.show()
    start_btn.show()

    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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

        screen.fill((0, 0, 0))
        title_text = font.render("Yahtzee", True, (255, 255, 255))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 120))

        left_btn.draw(screen)
        right_btn.draw(screen)
        start_btn.draw(screen)

        players_text = font.render(f"Liczba graczy: {num_players}", True, (255,255,255))
        screen.blit(players_text, (WIDTH // 2 - players_text.get_width() // 2, HEIGHT // 2 - players_text.get_height() // 2))

        pygame.display.flip()

    return num_players
def choose_difficulty():
    font = pygame.font.Font("fonts/font.ttf", 40)
    # Jeszcze większe przyciski poziomów
    easy_btn = Button(WIDTH // 2 - 140, 230, 280, 85, "Łatwy")
    medium_btn = Button(WIDTH // 2 - 140, 340, 280, 85, "Średni")
    hard_btn = Button(WIDTH // 2 - 140, 450, 280, 85, "Trudny")

    easy_btn.show()
    medium_btn.show()
    hard_btn.show()

    while True:
        screen.fill((0, 0, 0))
        title_text = font.render("Wybierz poziom trudności", True, (255, 255, 255))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 150))

        for btn in [easy_btn, medium_btn, hard_btn]:
            btn.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_btn.is_clicked(event.pos):
                    return None  # brak limitu
                elif medium_btn.is_clicked(event.pos):
                    return 40  # 40 sekund
                elif hard_btn.is_clicked(event.pos):
                    return 20  # 20 sekund
       
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
    num_players = main_menu()
    time_limit = choose_difficulty()  # None, 20 lub 10 sekund
    players = add_players(num_players)

    current_player_index = 0
    running = True
    turn_start_time = pygame.time.get_ticks()  # start tury
    timer_font = pygame.font.Font("fonts/font.ttf", 30)

    while running:
        current_player = players[current_player_index]
        scoreboard = current_player.scoreboard
        game_round = current_player.round

        current_time = pygame.time.get_ticks()
        if time_limit:
            time_left = max(0, time_limit - (current_time - turn_start_time) // 1000)
        else:
            time_left = None

        if time_limit and (current_time - turn_start_time) >= time_limit * 1000:
            # Czas minął – przejdź do następnego gracza
            current_player_index = (current_player_index + 1) % len(players)
            game_round.next_turn()
            turn_start_time = pygame.time.get_ticks()
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif not game_round.is_game_over() and event.type == pygame.MOUSEBUTTONDOWN:
                if game_round.roll_count > 0 and scoreboard.handle_click(event.pos, game_round.get_dices()):
                    current_player_index = (current_player_index + 1) % len(players)
                    game_round.next_turn()
                    turn_start_time = pygame.time.get_ticks()  # reset timera
                else:
                    event_result = game_round.handle_events(event, scoreboard, current_player.name, time_limit)
                    if event_result in ("roll", "reroll"):
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
                game_round.draw_game(scoreboard, current_player.name,time_limit)

                # Rysuj timer, jeśli jest limit czasu
                if time_left is not None:
                    if time_left < 5:
                        color = (255, 0, 0)  #  czerwony
                    elif time_left < 10:
                        color = (255, 255, 0)  #  żółty
                    else:
                        color = (255, 255, 255)  #  biały

                    timer_text = timer_font.render(f"Pozostały czas: {time_left} s", True, color)
                    screen.blit(timer_text, (WIDTH - timer_text.get_width() - 20, 20))
            else:
                current_player_index = (current_player_index + 1) % len(players)
                turn_start_time = pygame.time.get_ticks()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    exit()


if __name__ == "__main__":
    
    main()
