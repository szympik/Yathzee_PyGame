from collections import Counter 

class ScoreCategory:
    def __init__(self, name):
        """Inicjalizuje kategorię punktacji."""
        self.name = name

    def check(self, dice_values):
        """Sprawdza, czy dana kombinacja pasuje do tej kategorii."""
        raise NotImplementedError

    def score(self, dice_values):
        """Oblicza punkty dla danej kategorii."""
        raise NotImplementedError
    
class Ones(ScoreCategory):
    def __init__(self):
        """Kategoria: Jedynki."""
        super().__init__("Jedynki")

    def check(self, dice_values):
        return True

    def score(self, dice_values):
        return sum(value for value in dice_values if value == 1)

class Twos(ScoreCategory):
    def __init__(self):
        """Kategoria: Dwójki."""
        super().__init__("Dwójki")

    def check(self, dice_values):
        return True

    def score(self, dice_values):
        return sum(value for value in dice_values if value == 2)
    
class Threes(ScoreCategory):
    def __init__(self):
        """Kategoria: Trójki."""
        super().__init__("Trójki")

    def check(self, dice_values):
        return True

    def score(self, dice_values):
        return sum(value for value in dice_values if value == 3)
    
class Fours(ScoreCategory):
    def __init__(self):
        """Kategoria: Czwórki."""
        super().__init__("Czwórki")

    def check(self, dice_values):
        return True

    def score(self, dice_values):
        return sum(value for value in dice_values if value == 4)
    
class Fives(ScoreCategory):
    def __init__(self):
        """Kategoria: Piątki."""
        super().__init__("Piątki")

    def check(self, dice_values):
        return True

    def score(self, dice_values):
        return sum(value for value in dice_values if value == 5)
    
class Sixes(ScoreCategory):
    def __init__(self):
        """Kategoria: Szóstki."""
        super().__init__("Szóstki")

    def check(self, dice_values):
        return True

    def score(self, dice_values):
        return sum(value for value in dice_values if value == 6)

class ThreeOfAKind(ScoreCategory):
    def __init__(self):
        """Kategoria: Trójka."""
        super().__init__("Trójka")

    def check(self, dice_values):
        return any(dice_values.count(value) >= 3 for value in set(dice_values))

    def score(self, dice_values):
        return sum(dice_values) if self.check(dice_values) else 0

class FourOfAKind(ScoreCategory):
    def __init__(self):
        """Kategoria: Czwórka."""
        super().__init__("Czwórka")

    def check(self, dice_values):
        return any(dice_values.count(value) >= 4 for value in set(dice_values))

    def score(self, dice_values):
        return sum(dice_values) if self.check(dice_values) else 0
    
class FullHouse(ScoreCategory):
    def __init__(self):
        """Kategoria: Full House."""
        super().__init__("Full House")

    def check(self, dice_values):
        counts = Counter(dice_values)
        return len(counts) == 2 and any(count == 3 for count in counts.values())

    def score(self, dice_values):
        return 25 if self.check(dice_values) else 0

class SmallStraight(ScoreCategory):
    def __init__(self):
        """Kategoria: Mały Strit."""
        super().__init__("Mały Strit")

    def check(self, dice_values):
        unique_values = set(dice_values)
        return any(set(straight).issubset(unique_values) for straight in [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]])

    def score(self, dice_values):
        return 30 if self.check(dice_values) else 0
    
class LargeStraight(ScoreCategory):
    def __init__(self):
        """Kategoria: Duży Strit."""
        super().__init__("Duży Strit")

    def check(self, dice_values):
        unique_values = set(dice_values)
        return unique_values == {1, 2, 3, 4, 5} or unique_values == {2, 3, 4, 5, 6}

    def score(self, dice_values):
        return 40 if self.check(dice_values) else 0
    
class Yahtzee(ScoreCategory):
    def __init__(self):
        """Kategoria: Yahtzee."""
        super().__init__("Yahtzee")
    def check(self, dice_values):
        return len(set(dice_values)) == 1
    
    def score(self, dice_values):
        return 50 if self.check(dice_values) else 0
class Chance(ScoreCategory):
    def __init__(self):
        """Kategoria: Chance."""
        super().__init__("Chance")

    def check(self, dice_values):
        return True

    def score(self, dice_values):
        return sum(dice_values)