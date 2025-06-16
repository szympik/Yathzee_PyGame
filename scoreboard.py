import pygame
from _import import *


class Scoreboard:
    def __init__(self, x=50, y=50):
        """Inicjalizuje scoreboard z pozycją, rozmiarem i kategoriami."""
        self.font = pygame.font.Font("fonts/fancy_bold.ttf", 32)
        self.x, self.y = x, y
        self.width, self.height = 500, 950
        self.categories = [
            "Ones", "Twos", "Threes", "Fours", "Fives", "Sixes",
            "Three of a Kind", "Four of a Kind", "Full House",
            "Small Straight", "Large Straight", "Yahtzee", "Chance"
        ]
        self.rects = self.get_rect()
        self.values = {category: None for category in self.categories}
        self.img = pygame.image.load("img/scoreboard.png")

    def get_rect(self):
        """Zwraca listę prostokątów odpowiadających polom punktacji."""
        pom = 0
        rects = []
        for i, _ in enumerate(self.categories):
            if i < 6:
                rect = pygame.Rect(
                    self.x + 120, self.y + 125 + pom, 265, 45)
                pom += 55
            else:
                rect = pygame.Rect(
                    self.x + 120, self.y + 125 + pom, 265, 45)
                pom += 57
            rects.append(rect)
        return rects

    def draw(self, screen, dice_values=None, difficulty=None, roll_count=0):
        """Rysuje scoreboard na ekranie wraz z aktualnymi wynikami i podpowiedziami."""
        self.img = pygame.transform.scale(self.img, (self.width, self.height))
        screen.blit(self.img, (self.x, self.y))
        highlight = []
        highlight_scores = {}
        if (difficulty in (None, 40)) and dice_values and roll_count > 0:
            for i, category in enumerate(self.categories):
                if self.values[category] is None:
                    score = self.calculate_score(category, dice_values)
                    if score > 0:
                        highlight.append(category)
                        highlight_scores[category] = score

        for i, category in enumerate(self.categories):
            rect = self.rects[i]
            pygame.draw.rect(screen, TRANSPARENT, rect, 1)
            text = self.font.render(category, True, GOLD)
            screen.blit(text, (rect.x + 3, rect.y + 3))
            value = self.values[category]
            if category in highlight and value is None:
                val = highlight_scores[category]
                val_text = self.font.render(str(val), True, (255, 0, 0))
                screen.blit(val_text, (rect.right - 40, rect.y))
            elif value is not None:
                val_text = self.font.render(str(value), True, YELLOW)
                screen.blit(val_text, (rect.right - 40, rect.y))

    def handle_click(self, pos, dice_values):
        """Obsługuje kliknięcie w pole punktacji i przypisuje wynik."""
        for rect, category in zip(self.rects, self.categories):
            if rect.collidepoint(pos) and self.values[category] is None:
                self.values[category] = self.calculate_score(category, dice_values)
                return True
        return False

    def calculate_score(self, category, dice_values):
        """Oblicza wynik dla danej kategorii na podstawie wartości kości."""
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

    def total_score(self):
        """Zwraca sumę wszystkich zdobytych punktów."""
        return sum(value for value in self.values.values() if value is not None)

    def possible_categories(self, dice_values):
        """Zwraca listę możliwych kategorii do wybrania na podstawie aktualnych kości."""
        possible = []
        for category in self.categories:
            if self.values[category] is None:
                score = self.calculate_score(category, dice_values)
                if score > 0:
                    possible.append(category)
        return possible
