from _import import *
from dice import Dice
from button import Button


pygame.init()

# Ustawienia okna

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yahtzee")
music = pygame.mixer.Sound('sound/muza.mp3')
music.set_volume(0.0)  # Ustaw głośność dźwięku
music.play()

def cup_animation(screen):
        
        farame = 1
        total_frames = 6
        for frame in range(1, total_frames + 1):
            img_path = f"img/kubek_animacja/{frame}.png"
            if os.path.exists(img_path):
                img = pygame.image.load(img_path)
                
                    
font = pygame.font.Font(None, 36)

def score_test(dices):
    print("Threeofakind" if ThreeOfAKind().check(get_dices(dices)) else "False")
    print("Fourofakind" if FourOfAKind().check(get_dices(dices)) else "False")
    print("FullHouse" if FullHouse().check(get_dices(dices)) else "False")
    print("SmallStraight" if SmallStraight().check(get_dices(dices)) else "False")
    print("LargeStraight" if LargeStraight().check(get_dices(dices)) else "False")
    print("Yahtzee" if Yahtzee().check(get_dices(dices)) else "False")
    print("Ones:", Ones().score(get_dices(dices)))
    print("Twos:", Twos().score(get_dices(dices)))
    print("Threes:", Threes().score(get_dices(dices)))
    print("Fours:", Fours().score(get_dices(dices)))
    print("Fives:", Fives().score(get_dices(dices)))
    print("Sixes:", Sixes().score(get_dices(dices)))
    print("/n-----------------------------------/n")

def get_dices(dices):
    return [dice.get_value() for dice in dices]

def handle_events(event, dices, roll, reroll):

    if event.type == pygame.QUIT:
        return False
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if roll.is_clicked(event.pos):
            cup_animation(screen)
            for dice in dices:
                dice.start_roll(dices)
            roll.hide()
            reroll.show()
            
        elif reroll.is_clicked(event.pos):
            cup_animation(screen)
            for dice in dices:
                dice.reroll(dices)
            #score_test(dices)
            
            
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
             # Pobierz wartości wszystkich kostek
            
            
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
