# Yahtzee PyGame

Yahtzee PyGame to gra komputerowa oparta na klasycznej grze w kości Yahtzee, napisana w Pythonie z użyciem biblioteki PyGame. Gra umożliwia rozgrywkę dla 1-6 graczy, oferuje animacje, dźwięki, różne poziomy trudności oraz zapisywanie wyników do pliku tekstowego.

## Funkcje gry

- **Tryb wieloosobowy**: od 1 do 6 graczy, każdy z własnym scoreboardem.
- **Wybór poziomu trudności**: łatwy (bez limitu czasu), średni (40 sekund na turę), trudny (20 sekund na turę).
- **Animacje i dźwięki**: animowane rzuty kośćmi, dźwięki rzucania i potrząsania kubkiem.
- **Kategorie punktacji**: pełna lista kategorii Yahtzee (jedynki, dwójki, trójki, czwórki, piątki, szóstki, trójka, czwórka, full house, mały strit, duży strit, yahtzee, szansa).
- **Podpowiedzi**: podświetlanie możliwych do zdobycia punktów w danej turze.
- **Zapisywanie wyników**: po zakończeniu gry wyniki są zapisywane do pliku `scores.txt` wraz z datą.
- **Przyciski i interfejs**: graficzne przyciski do rzutów, ponownych rzutów, wyboru kategorii i restartu gry.

## Wymagania

- Python 3.10+
- Biblioteka [pygame](https://www.pygame.org/)
- Foldery z grafikami (`img/`), dźwiękami (`sound/`) oraz czcionkami (`fonts/`).

## Uruchomienie gry

1. Zainstaluj wymagane biblioteki:
    ```sh
    pip install pygame
    ```
2. Upewnij się, że w katalogu znajdują się wszystkie wymagane pliki graficzne, dźwiękowe i czcionki.
3. Uruchom grę:
    ```sh
    python game.py
    ```

## Struktura projektu

- `game.py` – główny plik uruchamiający grę i obsługujący pętlę gry.
- `round.py` – logika pojedynczej rundy, obsługa rzutów i końca gry.
- `scoreboard.py` – obsługa tablicy wyników i punktacji.
- `score_category.py` – implementacja kategorii punktacji Yahtzee.
- `dice.py` – animacje i logika pojedynczej kości.
- `button.py` – obsługa przycisków graficznych.
- `player.py` – obsługa gracza i wprowadzania imienia.
- `_import.py` – importy i stałe globalne (kolory, rozmiary okna).
- `scores.txt` – plik z zapisanymi wynikami gier.
- `fonts/`, `img/`, `sound/` – zasoby gry.

## Zasady gry

1. Każdy gracz po kolei wykonuje rzuty pięcioma kośćmi.
2. W każdej turze można wykonać do 3 rzutów, wybierając które kości przerzucić.
3. Po zakończeniu rzutów gracz wybiera kategorię punktacji, do której przypisuje wynik.
4. Gra kończy się po 13 turach każdego gracza.
5. Wygrywa gracz z najwyższą sumą punktów.

## Autor
Adrian Paluch i Adam Mus
Projekt stworzony na potrzeby nauki programowania w Pythonie oraz praktyki z biblioteką PyGame.

---

**Miłej zabawy!**