import copy
from car import Car

ORIENTATIONS = [0, 1]
MIN_CAR_SIZE = 2
MAX_CAR_SIZE = 4
Y = 0
X = 1
BOARD_SIZE = 7
EMPTY = '_'
END_CELL = (3, 7)
POSSIBLE_NAMES = ["Y", "B", "O", "W", "G", "R"]
UP = 'u'
DOWN = 'd'
LEFT = 'l'
RIGHT = 'r'


class Board:
    """
    this class will represent a board of 7 on 7 which will be used to play
    rush hour on with the class car.
    """
    def __init__(self):
        # Note that this function is required in your Board implementation.
        # However, is not part of the API for general board types.
        self.__size = BOARD_SIZE
        self.__victory_cell = END_CELL
        self.__car_list = []
        board = list()
        row = [EMPTY] * BOARD_SIZE
        for row_number in range(BOARD_SIZE):
            board.append(copy.deepcopy(row))
        self.__board = board

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        the_board = ""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if col == BOARD_SIZE - 1:
                    the_board += self.__board[row][col]
                else:
                    the_board += self.__board[row][col] + " "
            if row != BOARD_SIZE - 1:
                the_board += "\n"
        return the_board

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        cell_list = list()
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                cell_list.append((row, col))
        cell_list.append(self.__victory_cell)
        return cell_list

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description) 
                 representing legal moves
        """
        car_names = set()
        ans_tuples = list()
        # Go over all the Board in search for cars
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.__board[row][col] != EMPTY:
                    car_names.add(self.__board[row][col])
        for name in car_names:
            move_dict = dict()
            new_car = self.get_car_by_name(name)
            temp_car = Car(new_car.get_name(), new_car.get_length(),
                           new_car.get_location(), new_car.get_orientation())
            move_dict.update(new_car.possible_moves())
            for move in move_dict:
                if self.move_car(new_car.get_name(), move):
                    ans_tuples.append((new_car.get_name(), move,
                                       move_dict[move]))
                    self.reverse_move_car(new_car.get_name(), move)
        return ans_tuples

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be
        filled for victory.
        :return: (row,col) of goal location
        """
        return self.__victory_cell

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        if coordinate == self.get_victory_cell():
            return None
        if self.__board[coordinate[Y]][coordinate[X]] == EMPTY:
            return None
        else:
            return self.__board[coordinate[Y]][coordinate[X]]

    def check_car_placement(self, car):
        """
        checks if the car given can be placed on the board.
        :param car: the car we check
        :return: True if it can be places and False otherwise
        """
        car_coordinates = car.car_coordinates()
        for point in car_coordinates:
            if not (0 <= point[X] < BOARD_SIZE and 0 <= point[Y]
                    < BOARD_SIZE):
                return False
            if self.__board[point[Y]][point[X]] != EMPTY:
                return False
        if not (isinstance(car.get_name(), str) and
                car.get_name() in POSSIBLE_NAMES):
            return False
        if not MIN_CAR_SIZE <= car.get_length() <= MAX_CAR_SIZE:
            return False
        if car.get_orientation() not in ORIENTATIONS:
            return False
        return True

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        car_coordinates = car.car_coordinates()
        # Sanity check
        if not self.check_car_placement(car):
            return False
        # Actual placement
        for point in car_coordinates:
            self.__board[point[Y]][point[X]] = car.get_name()
        # Add car to list
        self.__car_list.append(car)
        return True

    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: (str) name of the car to move
        :param movekey: (str) Key of move in car to activate
        :return: True upon success, False otherwise
        """
        car = self.get_car_by_name(name)
        # If the car doesnt exist
        if car is None:
            return False
        else:
            # Save car to temp to delete from board later or return to it
            temp_car = Car(car.get_name(), car.get_length(),
                           car.get_location(), car.get_orientation())
            # If the car cant be moved
            if not car.move(movekey):
                return False
            else:
                for location in car.car_coordinates():
                    if self.__board[location[Y]][location[X]] != EMPTY and \
                            self.__board[location[Y]][location[X]] != name:
                        car = Car(temp_car.get_name(), temp_car.get_length(),
                                  temp_car.get_location(),
                                  temp_car.get_orientation())
                        return False
                # Remove the car from the board and add it in the new location
                for board_car in self.__car_list:
                    if board_car.get_location() == temp_car.get_location():
                        self.__car_list.remove(board_car)
                for location in temp_car.car_coordinates():
                    self.__board[location[Y]][location[X]] = EMPTY
                self.add_car(car)
                return True

    def reverse_move_car(self, name, movekey):
        if movekey == UP:
            self.move_car(name, DOWN)
        if movekey == DOWN:
            self.move_car(name, UP)
        if movekey == RIGHT:
            self.move_car(name, LEFT)
        if movekey == LEFT:
            self.move_car(name, RIGHT)

    def get_car_by_name(self, name):
        """
        gets the location of the car with the name given on the board.
        :param name: (str) the cars name we are searching for.
        :return: (tuple) the location of the car or None if it isn't on the
        board.
        """
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.__board[row][col] == name:
                    return self.get_car_from_location_and_name((row, col),
                                                               name)
        return None

    def get_car_from_location_and_name(self, location, name):
        """
        generates a car object from the location given.
        :param location: (tuple) the start location of a car.
        :param name: (str) name of the car we are looking for.
        :return: (car) the car object on the board.
        """
        orientation = -1
        length = 1
        if location[Y] + MAX_CAR_SIZE >= BOARD_SIZE:
            y_size = BOARD_SIZE
        else:
            y_size = location[Y] + MAX_CAR_SIZE
        if location[X] + MAX_CAR_SIZE >= BOARD_SIZE:
            x_size = BOARD_SIZE
        else:
            x_size = location[X] + MAX_CAR_SIZE

        if location[Y] + 1 <= BOARD_SIZE - 1 and \
                self.__board[location[Y] + 1][location[X]] == name:
            orientation = 0
            for position in range(location[Y] + 1, y_size):
                if self.__board[position][location[X]] == name:
                    length += 1
        elif location[X] + 1 <= BOARD_SIZE - 1 and \
                self.__board[location[Y]][location[X] + 1] == name:
            orientation = 1
            for position in range(location[X] + 1, x_size):
                if self.__board[location[Y]][position] == name:
                    length += 1
        return Car(name, length, location, orientation)

    def set_point(self, point, value):
        """
        sets the point in the board to be a new value.
        :param point: (tuple) the point we want to change.
        :param value: (string) the new value for the point in the board.
        :return: None if the set is invalid (bad point ot not string).
        """
        if 0 <= point[X] <= BOARD_SIZE and 0 <= point[Y] <= BOARD_SIZE and \
                isinstance(value, str):
            self.__board[point[Y]][point[X]] = value
        else:
            return None

    def get_car_list(self):
        """
        :return: (list) the list of cars on the board
        """
        return self.__car_list

    def get_victory_cell(self):
        """
        :return: (tuple) the victory cell
        """
        return self.__victory_cell