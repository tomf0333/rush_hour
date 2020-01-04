VERTICAL = 0
HORIZONTAL = 1
Y = 0
X = 1
UP = 'u'
DOWN = 'd'
LEFT = 'l'
RIGHT = 'r'
BOARD_SIZE = 7
CELL = 0


class Car:
    """
    This class represents cars that are used in the rush hour game,
    each car has a name, length, location and orientation, can move only in its
    orientation and only one space.
    """
    def __init__(self, name="", length=0, location=(0, 0), orientation=-1):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        can be between 2 and 4, including.
        :param location: A tuple representing the car's head (row, col)
        location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        self.__name = name
        self.__length = length
        self.__location = location
        self.__orientation = orientation

    def __str__(self):
        """
        :return: a string representation of object Car.
        """
        return "Car " + self.__name + " is in: " + str(self.car_coordinates())

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        location_list = list()
        coordinate_y_start, coordinate_x_start = self.__location
        if self.__orientation == HORIZONTAL:
            for point in range(self.__length):
                location_list.append((coordinate_y_start,
                                      coordinate_x_start + point))
        elif self.__orientation == VERTICAL:
            for point in range(self.__length):
                location_list.append((coordinate_y_start + point,
                                      coordinate_x_start))
        return location_list

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements
        permitted by this car.
        """
        car_loc = self.get_location()
        car_end = self.get_car_end()
        moves_dict = dict()
        if self.__orientation == VERTICAL:
            if car_loc[Y] - 1 >= 0:
                moves_dict[UP] = "the car moves up because it saw the movie"\
                        " and was like yea..."
            if car_end[Y] + 1 <= BOARD_SIZE - 1:
                moves_dict[DOWN] = "the car moves down because i told it so"\
                        " and it is a wimp"
        elif self.__orientation == HORIZONTAL:
            if car_loc[X] - 1 >= 0:
                moves_dict[LEFT] = "its just a jump to the left..."
            if car_end[X] + 1 <= BOARD_SIZE - 1:
                moves_dict[RIGHT] = "and then a step to riiiiiight"
            # with your hands on your hips
            # you bring your knees in tiiiight
            # but its the pelvic thruuuuust
            # that really drives you insaenenene
        return moves_dict

    def movement_requirements(self, movekey):
        """
        see what point in the board is required for a given car to move in a
        given direction.
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for
        this move to be legal.
        """
        car_start = self.__location
        car_end = self.get_car_end()
        if movekey == UP:
            return [(car_start[Y] - 1, car_start[X])]
        if movekey == DOWN:
            return [(car_end[Y] + 1, car_end[X])]
        if movekey == LEFT:
            return [(car_start[Y], car_start[X] - 1)]
        if movekey == RIGHT:
            return [(car_end[Y], car_end[X] + 1)]

    def move(self, movekey):
        """
        moves the car in the direction given.
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        current_loc = self.__location
        orientation = self.__orientation
        next_loc = self.movement_requirements(movekey)
        # Not possible moves
        if movekey == UP and orientation == HORIZONTAL or\
                movekey == DOWN and orientation == HORIZONTAL or\
                movekey == RIGHT and orientation == VERTICAL or\
                movekey == LEFT and orientation == VERTICAL:
            return False
        # If the location to move to is ok then move
        if 0 <= next_loc[CELL][Y] <= BOARD_SIZE - 1 and\
                0 <= next_loc[CELL][X] <= BOARD_SIZE - 1:
            if movekey == UP:
                self.set_location((current_loc[Y] - 1, current_loc[X]))
            if movekey == DOWN:
                self.set_location((current_loc[Y] + 1, current_loc[X]))
            if movekey == RIGHT:
                self.set_location((current_loc[Y], current_loc[X] + 1))
            if movekey == LEFT:
                self.set_location((current_loc[Y], current_loc[X] - 1))
            return True
        return False

    # All the Gets
    def get_name(self):
        """
        :return: a string representing the name of the given car.
        """
        return self.__name

    def get_location(self):
        """
        :return: a tuple representing the location of a given car
        its most left and up point.
        """
        return self.__location

    def get_orientation(self):
        """
        :return: an int representing the orientation of a given car
        1 for horizontal and 0 for vertical
        """
        return self.__orientation

    def get_length(self):
        """
        :return: an int representing the length of a given car
        """
        return self.__length

    def get_car_end(self):
        """
        :return: a tuple representing the end point of a given car
        its rightest and lowest point.
        """
        location = self.__location
        length = self.__length
        orientation = self.__orientation
        # If it is horizontal then add to its column side
        if orientation == HORIZONTAL:
            return location[Y], location[X] + length - 1
        # If it is vertical then add to its row side
        if orientation == VERTICAL:
            return location[Y] + length - 1, location[X]

    # All the sets
    def set_location(self, new_location):
        """
        changes the location of a given car.
        :param new_location: a tuple representing the new location
        :return: doesnt return
        """
        self.__location = new_location
