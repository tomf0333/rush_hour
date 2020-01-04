from board import *
from car import *
import helper as h
import sys
import copy

JSON_FILE = 1
CELL_Y = 0
CELL_X = 1
NAME = 0
PSICK = 1
DIRECTION = 2
LENGTH = 0
LOCATION = 1
ORIENTATION = 2
DIRECTIONS = ["d", "r", "l", "u"]
CAR_NAMES = ["O", "Y", "R", "G", "B", "W"]
CHOOSE_GUI = "specify which car you want to move(name) and what direction" \
             "(from ['d','r','u','l']) seperated by a ',': "


class Game:
    """
    this class will work with the Board and Car classes to make the full
    Rush Hour™ game
    """

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: (board) An object of type board
        """
        file = h.load_json(sys.argv[JSON_FILE])
        for car in file:
            new_car = Car(car, file[car][LENGTH], file[car][LOCATION],
                          file[car][ORIENTATION])
            board.add_car(new_car)
        self.__game_board = board

    def __single_turn(self):
        """
        does a single tun of the game.
        :return: does not return, moves cars on the board.
        """
        play_choice = input(CHOOSE_GUI)
        while not check_input(play_choice):
            play_choice = input(CHOOSE_GUI)
        play_name, play_dir = play_choice[NAME], play_choice[DIRECTION]
        self.__game_board.move_car(play_name, play_dir)

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        print(self.get_game_board())
        while not self.__win():
            self.__single_turn()
            print(self.get_game_board())
        print("\nyatta!!!")

    def __win(self):
        """
        this method checks if you won, by having a car at the right place so
        one step right would be in the victory cell, which isnt on the board.
        :return: True if you won and False otherwise
        """
        victory_cell = self.__game_board.get_victory_cell()
        real_victory = (victory_cell[Y], victory_cell[X] - 1)
        if self.__game_board.cell_content(real_victory) is not None:
            return True
        return False

    def get_game_board(self):
        """
        :return: the board that the game is playing on.
        """
        return self.__game_board


def check_input(inp):
    """
    checks that the input is a valid input for the game
    :param inp: (string) the given input (choice) from the game interface
    :return: True if the choice is valid and false otherwise
    """
    if len(inp) != 3:
        print("\nwrong length")
        return False
    if inp[PSICK] != ',':
        print("\nno ','")
        return False
    if inp[NAME] not in CAR_NAMES:
        print("\nbad name")
        return False
    if inp[DIRECTION] not in DIRECTIONS:
        print("\nbad direction")
        return False
    return True

if __name__== "__main__":
    board = Board()
    game = Game(board)
    Game.play(game)
