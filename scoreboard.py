import pygame
from score_category import *

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

class Scoreboard:
    def __init__(self, x, y):
        self.font = pygame.font.Font(None, 32)
        self.x, self.y = x, y
        self.width, self.height = 250, 40

        self.categories = [
            "Ones", "Twos", "Threes", "Fours", "Fives", "Sixes",
            "Three of a Kind", "Four of a Kind", "Full House",
            "Small Straight", "Large Straight", "Yahtzee", "Chance"
        ]
        self.rects = []
        self.values = {category: None for category in self.categories}

        for i, _ in enumerate(self.categories):
            rect = pygame.Rect(x, y + i * self.height, self.width, self.height)
            self.rects.append(rect)

    def draw(self, screen):
        for i, category in enumerate(self.categories):
            rect = self.rects[i]
            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, WHITE, rect, 2)

            text = self.font.render(category, True, BLACK)
            screen.blit(text, (rect.x + 5, rect.y + 5))

            value = self.values[category]
            if value is not None:
                val_text = self.font.render(str(value), True, BLACK)
                screen.blit(val_text, (rect.right - 40, rect.y + 5))

    def handle_click(self, pos, dice_values):
        for rect, category in zip(self.rects, self.categories):
            if rect.collidepoint(pos) and self.values[category] is None:
                self.values[category] = self.calculate_score(category, dice_values)

    def calculate_score(self, category, dice_values):
        if category == "Ones":
            return Ones().score(dice_values)
        elif category == "Twos":
            return Twos().score(dice_values)
        elif category == "Threes":
            return Threes().score(dice_values)
        elif category == "Fours":
            return Fours().score(dice_values)
        elif category == "Fives":
            return Fives().score(dice_values)
        elif category == "Sixes":
            return Sixes().score(dice_values)
        elif category == "Three of a Kind":
            return ThreeOfAKind().score(dice_values)
        elif category == "Four of a Kind":
            return FourOfAKind().score(dice_values)
        elif category == "Full House":
            return FullHouse().score(dice_values)
        elif category == "Small Straight":
            return SmallStraight().score(dice_values)
        elif category == "Large Straight":
            return LargeStraight().score(dice_values)
        elif category == "Yahtzee":
            return Yahtzee().score(dice_values)
        elif category == "Chance":
            return Chance().score(dice_values)
        else:
            return 0
