import os
import json
import random
from cursor import Cursor
from tile import Tile


def enable_vt100() -> None:
    """Enables vt100.

    A Windows thing. Have to do this to use escape codes, which I used for colour.
    """

    if os.name == "nt":
        os.system("")


def get_colour(colour : str, bright : bool = False) -> str:
    colours = {
        "black": 30,
        "red": 31,
        "green": 32,
        "yellow": 33,
        "blue": 34,
        "purple": 35,
        "cyan": 36,
        "white": 37
    }
    if bright:
        return f"\033[1;{colours[colour]};40m"
    return f"\033[0;{colours[colour]};40m"


def clear_screen() -> None:
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def generate_mine_field(width : int = 20, height : int = 10, mines : int = 20) -> None:
    minefield = []
    for x in range(width):
        new_line = []
        for y in range(height):
            new_line.append(Tile())
        minefield.append(new_line)

    for i in range(mines):
        minefield[random.randint(1, width) - 1][random.randint(1, height) - 1].has_mine = True

    return minefield


def get_number_of_mines(x : int, y : int, minefield : list) -> int:
    counter = 0
    if x > 0:
        if minefield[x - 1][y].has_mine:
            counter += 1
        if y > 0:
            if minefield[x - 1][y - 1].has_mine:
                counter += 1
        if y < len(minefield[0]) - 1:
            if minefield[x - 1][y + 1].has_mine:
                counter += 1
    
    if x < len(minefield) - 1:
        if minefield[x + 1][y].has_mine:
            counter += 1
        if y > 0:
            if minefield[x + 1][y - 1].has_mine:
                counter += 1
        if y < len(minefield[0]) - 1:
            if minefield[x + 1][y + 1].has_mine:
                counter += 1
    
    if y > 0:
        if minefield[x][y - 1].has_mine:
            counter += 1
    if y < len(minefield[0]) - 1:
        if minefield[x][y + 1].has_mine:
            counter += 1
    
    return counter


def get_uncovered_character(number_of_mines : int) -> str:
    """Gets the correct character for a number tile.

    Args:
        number_of_mines (int): The number of mines surrounding the tile.

    Returns:
        str: The character representation of the tile.
    """
    if number_of_mines == 0:
        return "."
    return str(number_of_mines)


def get_tile_character(x : int, y : int, minefield : list, dead : bool = False):
    number_colours = {
        ".": "white",
        "1": "blue",
        "2": "green",
        "3": "red",
        "4": "purple",
        "5": "yellow",
        "6": "cyan",
        "7": "white",
        "8": "white"
    }
    
    if minefield[x][y].has_flag and not dead:
        return get_colour("red") + "|"
    if not minefield[x][y].uncovered and not dead:
        return get_colour("white") + "#"
    if minefield[x][y].has_mine:
        return get_colour("white") + "*"
    char = get_uncovered_character(get_number_of_mines(x, y, minefield))
    return get_colour(number_colours[char]) + char


def floodfill_uncover(x : int, y : int, minefield : list) -> list:
    """Uncovers tiles in a recursive floodfill algorithm. Used to reveal 0's.

    Not a great implementation but it's a high school programming internal so I'm
    just gonna leave it pretty scuffed.

    Args:
        x (int): X location.
        y (int): Y location.
        minefield (list): 2D list of tiles.

    Returns:
        list: Modified 2D list of tiles.
    """

    queue = []
    # Check Tile (x - 1)
    if x > 0:
        if minefield[x - 1][y].uncovered == False:
            minefield[x - 1][y].uncovered = True
            if get_tile_character(x - 1, y, minefield)[-1] == ".":
                queue.append((x - 1, y))
        
        # Check Tile (x - 1, y - 1)
        if y > 0:
            if minefield[x - 1][y - 1].uncovered == False:
                minefield[x - 1][y - 1].uncovered = True
                if get_tile_character(x - 1, y - 1, minefield)[-1] == ".":
                    queue.append((x - 1, y - 1))
                
        # Check tile (x - 1, y + 1)
        if y < len(minefield[0]) - 1:
            if minefield[x - 1][y + 1].uncovered == False:
                minefield[x - 1][y + 1].uncovered = True
                if get_tile_character(x - 1, y + 1, minefield)[-1] == ".":
                    queue.append((x - 1, y + 1))

    # Check tile (x + 1)
    if x < len(minefield) - 1:
        if minefield[x + 1][y].uncovered == False:
            minefield[x + 1][y].uncovered = True
            if get_tile_character(x + 1, y, minefield)[-1] == ".":
                queue.append((x + 1, y))
        
        # Check tile (x + 1, y - 1)
        if y > 0:
            if minefield[x + 1][y - 1].uncovered == False:
                minefield[x + 1][y - 1].uncovered = True
                if get_tile_character(x + 1, y - 1, minefield)[-1] == ".":
                    queue.append((x + 1, y - 1))

        # Check tile (x + 1, y + 1)
        if y < len(minefield[0]) - 1:
            if minefield[x + 1][y + 1].uncovered == False:
                minefield[x + 1][y + 1].uncovered = True
                if get_tile_character(x + 1, y + 1, minefield)[-1] == ".":
                    queue.append((x + 1, y + 1))
    
    # Check tile (y - 1)
    if y > 0:
        if minefield[x][y - 1].uncovered == False:
            minefield[x][y - 1].uncovered = True
            if get_tile_character(x, y - 1, minefield)[-1] == ".":
                queue.append((x, y - 1))

    # Check tile (y + 1)
    if y < len(minefield[0]) - 1:
        if minefield[x][y + 1].uncovered == False:
            minefield[x][y + 1].uncovered = True
            if get_tile_character(x, y + 1, minefield)[-1] == ".":
                queue.append((x, y + 1))

    for coord in queue:
        minefield = floodfill_uncover(coord[0], coord[1], minefield)
    
    return minefield


def print_mine_field(minefield : list, cursor : Cursor, dead : bool = False) -> None:
    """Prints game map.

    Args:
        minefield (list): The game map.
        cursor (Cursor): X and Y coordinates of the player's cursor.
        dead (bool, optional): Whether or not the player has lost. Defaults to False.
    """

    for y in range(len(minefield[0])):
        line = ""
        for x in range(len(minefield)):
            if x == cursor.x and y == cursor.y and not dead:
                line += get_colour(cursor.colour) + "+"
            else:
                line += get_tile_character(x, y, minefield, dead)
            if x < len(minefield) - 1:
                line += " "
        print(line)
    print(get_colour("white"))
    print(f"Hovering Over: {get_tile_character(cursor.x, cursor.y, minefield)}")
    print(get_colour("white"))


def print_ui() -> None:
    """Prints the game UI.
    """

    print("WASD to move, E to uncover, F to flag")
    print("? to open help")


def render_frame(minefield : list, cursor : Cursor) -> None:
    print_mine_field(minefield, cursor)
    print_ui()


settings = {}
with open("settings.json", "r") as f:
    settings = json.load(f)


controls = settings["controls"]


enable_vt100()
minefield = generate_mine_field()
cursor = Cursor(settings["cursor_colour"])


in_game = True
while in_game:
    clear_screen()
    render_frame(minefield, cursor)

    user_in = input(">").lower()

    if user_in == controls["up"]:
        if cursor.y > 0:
            cursor.y -= 1
    elif user_in == controls["left"]:
        if cursor.x > 0:
            cursor.x -= 1
    elif user_in == controls["down"]:
        if cursor.y < len(minefield[0]) - 1:
            cursor.y += 1
    elif user_in == controls["right"]:
        if cursor.x < len(minefield) - 1:
            cursor.x += 1
    elif user_in == controls["uncover"]:
        minefield[cursor.x][cursor.y].uncovered = True
        if get_tile_character(cursor.x, cursor.y, minefield)[-1] == ".":
            minefield = floodfill_uncover(cursor.x, cursor.y, minefield)
        in_game = not minefield[cursor.x][cursor.y].has_mine
    elif user_in == controls["flag"]:
        minefield[cursor.x][cursor.y].has_flag = not minefield[cursor.x][cursor.y].has_flag
    elif user_in == controls["quit"]:
        raise SystemExit


clear_screen()
print_mine_field(minefield, cursor, True)
print("You Died")
input("Press enter to exit")