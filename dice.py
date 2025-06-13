from _import import *

class Dice:
    def __init__(self, final_x=None, final_y=None):
       
        self.total_frames = 17
        self.images = {}
        self.load_images()
        self.is_rolling = False
        self.current_frame = 1
        self.current_dice = 1
        self.animation_speed = 1
        self.frame_counter = 0
        self.start_pos = (WIDTH - 170, HEIGHT - 240)
        self.current_pos = self.start_pos
        self.end_pos = (final_x, final_y)
        self.animation_progress = 0
        self.selected = False
        self.rect = pygame.Rect(final_x, final_y, 100, 100)
        self.dice_sound = pygame.mixer.Sound("sound/dice_roll.mp3")
        self.dice_sound.set_volume(0.1)
        self.previous_pos = self.start_pos

    def load_images(self):
        for dice_num in range(1, 7):
            self.images[dice_num] = {}
            for frame in range(1, self.total_frames + 1):
                img_path = f"img/animacje_kostki/{dice_num}/{frame}.png"
                if os.path.exists(img_path):
                    img = pygame.image.load(img_path)
                    self.images[dice_num][frame] = pygame.transform.scale(img, (100, 100))

    def start_roll(self,Dices):
        if not self.is_rolling:

            self.is_rolling = True
            self.end_pos = Dice.random_position(Dices)
            self.current_frame = 1
            self.current_dice = random.randint(1, 6)
            self.frame_counter = 0
            self.current_pos = self.start_pos
           
            self.animation_progress = 0
            self.dice_sound.play()

    def reroll(self,Dices):
        if not self.is_rolling and not self.selected:
            self.end_pos = Dice.random_position(Dices)
            self.current_pos = self.start_pos
            self.is_rolling = True
            self.current_frame = 1
            self.current_dice = random.randint(1, 6)
            self.frame_counter = 0
            self.animation_progress = 0
            
            self.dice_sound.play()
            

    def update(self):
        if self.is_rolling:
            self.frame_counter += 1
            if self.frame_counter >= self.animation_speed:
                self.frame_counter = 0
                self.current_frame += 1
                self.animation_progress += 1 / self.total_frames
                if self.animation_progress <= 1:
                    self.current_pos = (
                        int(self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * self.animation_progress),
                        int(self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * self.animation_progress)
                    )
                if self.current_frame > self.total_frames:
                    self.is_rolling = False
                    self.current_frame = self.total_frames
                    self.current_pos = self.end_pos

    def draw(self, surface):
        if self.current_dice in self.images and self.current_frame in self.images[self.current_dice]:
            surface.blit(self.images[self.current_dice][self.current_frame], self.current_pos)
            if self.selected:
                pygame.draw.rect(surface,(226, 172, 0), (self.current_pos[0]+12,self.current_pos[1]+12, 77, 77), 4)

    def toggle_selected(self, pos):
        rect = pygame.Rect(*self.current_pos, 100, 100)
        if rect.collidepoint(pos) and not self.is_rolling:
            self.selected = not self.selected

    @staticmethod
    def add_dice():
        dices = []
        for _ in range(5):
            final_x, final_y = Dice.random_position(dices)
            dice = Dice(final_x, final_y)
            dices.append(dice)
        return dices

    
    
    @staticmethod
    def random_position(dices,attempts=0):
        
        final_x = random.randint(750, 1550)  
        final_y = random.randint(150, 550)
        for dice in dices:
            if final_x in range(dice.end_pos[0]-128 , dice.end_pos[0] + 128) and final_y in range(dice.end_pos[1]-128 , dice.end_pos[1] + 128):
                attempts+=1
                if attempts > 100:
                    print("Nie można znaleźć idealnej pozycji, zwracam bezpieczną")
                    return final_x, final_y
                else:
                    return Dice.random_position(dices,attempts)
        
        
        return final_x, final_y 
    
    def get_value(self):
        
            return self.current_dice
    
    def reset(self):
        self.is_rolling = False
        self.current_frame = 1
        self.current_dice = 1
        self.frame_counter = 0
        self.current_pos = self.start_pos
        self.end_pos = (self.start_pos[0], self.start_pos[1])
        self.animation_progress = 0
        self.selected = False
        self.rect.topleft = (self.start_pos[0], self.start_pos[1])
        
   
        