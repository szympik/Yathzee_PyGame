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
def draw_cup(screen):
    cup_image = pygame.image.load("img/kubek_animacja/6.png")
    cup_image = pygame.transform.scale(cup_image, (400, 400))
    cup_x = WIDTH - 300
    cup_y = HEIGHT - 350
    screen.blit(cup_image, (cup_x, cup_y))

def cup_animation(screen):
    total_frames = 6
    images = {}
    
    # Ładowanie klatek animacji
    for frame in range(1, total_frames + 1):
        img_path = f"img/kubek_animacja/{frame}.png"
        if os.path.exists(img_path):
            img = pygame.image.load(img_path)
            images[frame] = pygame.transform.scale(img, (400, 400))
    
    # Pozycja w prawym dolnym rogu
    cup_x = WIDTH - 300
    cup_y = HEIGHT - 350
    
    current_frame = 1
    frame_counter = 0
    animation_speed = 2 # Szybkość animacji
    
    
    # Dźwięk kubka
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
        
       
        
        # Rysowanie obecnej klatki
        if current_frame <= total_frames and current_frame in images:
            screen.blit(images[current_frame], (cup_x, cup_y))
        
        
        pygame.display.flip()
        clock.tick(120)
        
        
    draw_cup(screen)
    cup_sound.stop()
                
                    
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
background = pygame.image.load("img/dice_background.png")  # jeśli masz tło
background = pygame.transform.scale(background, (1200, 800))

def draw_game(screen, dices, roll, reroll):
    screen.fill(BLACK)  
    
    screen.blit(background, (600, 0))
    draw_cup(screen)  # Ramka wokół planszy
    for dice in dices:
       dice.draw(screen)
    roll.draw(screen)
    reroll.draw(screen)
   
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
        clock.tick(200)
 
    pygame.quit()
    exit()

if __name__ == "__main__":
    main()
