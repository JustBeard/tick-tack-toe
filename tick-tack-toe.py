#!/usr/bin/env python3

#This program is the realization of the game "Tic-Tac-Toe" on the basis 
#of the MVC pattern. 
#
#Author: Khort Yevgen
#Version: 1.0

def main():
    model = TTTModelScale()
    controller = TTTController(model)

import abc
import copy

#*****************************************************************************
#*******************************  MODEL  *************************************
#*****************************************************************************

class TTTModelInterface(metaclass = abc.ABCMeta):
    """ Class is the interface model of the MVC pattern.
    """

    @abc.abstractmethod
    def __init__(self, model):
        pass

    @abc.abstractmethod
    def registerObserver(self, observer):
        pass

    @abc.abstractmethod
    def notifyObserver(self):
        pass

    @abc.abstractmethod
    def startPlay(self):
        pass

    @abc.abstractmethod
    def checkWinner(self):
        pass    

    @abc.abstractmethod
    def getData(self):
        pass

    @abc.abstractmethod
    def setCell(self, x, y):
        pass


class TTTModelScale(TTTModelInterface):
    """This class acts as a model in MVC pattern. Responsible for logic and 
    data game "Tic-Tac-Toe." If necessary, notify the view and controller of 
    changes of state.
    """

    def __init__(self):
        """The method initializes the data model and sets the initial values.
        """
        #The default size of the field equals to 3
        self.size = 3
        #Initialization of players
        self.__player_0 = "Zero Player"
        self.__player_X = "Cross Player"
        #Initialize the active player (current player). 
        #The first move is made by the player that controlls the cross.
        self.__active_player = self.__player_X
        #Flag of the end of the game
        self.__flag_end = False
        #Flag of the draws
        self.__flag_draw = False
        #List of observers
        self.__observers = []
        #Play-field TTT
        self.__field = []
    
    def registerObserver(self, observer):
        """Adds to the list of observers.
        """
        self.__observers.append(observer)

    def notifyObserver(self):
        """Posts observers status changes
        """
        for observer in self.__observers:
            observer.updateCurrentSituation()

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, size):
        self.__size = size

    def startPlay(self):
        """Creates a playing field and runs the algorithm of game.
        """
        #Creating a playing field that is filled with spaces
        buffer = [y for y in " "*self.size]
        self.__field = [list(buffer) for y in range(0, self.size)]
        #Posts observer status changes
        self.notifyObserver()

    def getData(self):
        """Gets data about current state. 
        """
        return (copy.copy(self.__size), copy.copy(self.__flag_end),
                copy.copy(self.__flag_draw), copy.copy(self.__active_player),
                copy.copy(self.__field))

    def isFullField(self):
        """Checks if a playing field is filled. If the field is filled and
        there is no winner, then game ends in a draw.
        """
        for line in self.__field:
            for column in line:
                if column == " ":
                    return False
        return True

    def checkWinner(self):
        """Checks if the game has ended in the case of a win
        """
        #Counts the number of X's and O's
        count_X = 0
        count_0 = 0
        #Counts the number of X's and 0's on reverse diagonal
        count_X_diagonal_rev = 0
        count_0_diagonal_rev = 0
        #Searches horizontal solid line
        for line in self.__field:
            for column in line:
                if column == "X":
                    count_X += 1
                elif column == "0":
                    count_0 += 1
            if count_X == self.size or count_0 == self.size:
                return True
            count_X, count_0 = 0, 0
        #Searches vertical solid line
        for column in range(0, self.size):
            for line in self.__field:
                if line[column] == "X":
                    count_X += 1
                elif line[column] == "0":
                    count_0 += 1
            if count_X == self.size or count_0 == self.size:
                return True
            count_X, count_0 = 0, 0
        #Searches diagonal solid line
        for line in range(0, self.size):
            for column in range(0, self.size):
                if line == column:
                    if self.__field[line][column] == "X":
                        count_X += 1
                    elif self.__field[line][column] == "0":
                        count_0 += 1
                if line == self.size - 1 - column:
                    if self.__field[line][column] == "X":
                        count_X_diagonal_rev += 1
                    elif self.__field[line][column] == "0":
                        count_0_diagonal_rev += 1
        if (self.size in 
                (count_X, count_0, count_X_diagonal_rev, count_0_diagonal_rev)):
            return True
        return False

    def nextStep(self):
        """Method that runs all the checks and determines the next
        active player.
        """
        #Checks winner
        self.__flag_end = self.checkWinner()
        if not self.__flag_end:
            #checks draw 
            self.__flag_draw = self.isFullField()
            if not self.__flag_draw:
                #If not end then change active player
                if self.__active_player == self.__player_X:
                    self.__active_player = self.__player_0
                else:
                    self.__active_player = self.__player_X
        #Posts observer status changes
        self.notifyObserver()

    def setCell(self, x, y):
        """Sets the value of the next cell and starts checking
        """
        if self.__active_player == self.__player_X:
            self.__field[x][y] = "X"
        else:
            self.__field[x][y] = "0"
        #Starts checking
        self.nextStep()


#*****************************************************************************
#******************************   VIEW   *************************************
#*****************************************************************************

class ObserverInterface(metaclass=abc.ABCMeta):
    """Interface of class for observers
    """

    @abc.abstractmethod
    def updateCurrentSituation(self):
        """The method that will be called by the observer when changing model.
        """
        pass


class TTTView(ObserverInterface):
    """This class acts as a view in MVC pattern. Responsible for displaying
    the current information and dialogue with the user.
    """
    
    def __init__(self, controller, model):
        self.__model = model
        self.__controller = controller
        #registration of the view in list of observers model
        self.__model.registerObserver(self)

    def printStartMessage(self):
        """Outputs greeting and information about the game to the console.
        """
        
        message = """
Hello!!!
This is a very cool game - Tick-Tack-Toe.
You can play on standart field (3x3) or set your own size of field.
"""
        print(message)
        message = "Will you play on the standart field (y/n)?:"
        #Queries a response from the user to choose the playing field.
        while True:
            line = input(message)
            if not line:
                #If the user has not entered, then put the default value.
                line = "y"
                break
            else:
                if line in ("y", "n"):
                    break
                else:
                    print("\nWarning!!! Value must be 'y' or 'n'\n")
        if line == "y":
            #Starts the game with the standart sizes
            self.__controller.startWithStandartSize()
        else:
            #Starts the game with the non standart sizes
            self.__controller.startWithNoStandartSize()

    def queryChangeSize(self):
        """Asks the user about new sizes for playing fields
        """
        msg = "Please, set size of side (number):"
        while True:
            try:
                line = input(msg)
                if not line:
                    #If the user has not entered, then put the default value.
                    return 3
                i = int(line)
                if i < 3:
                    print("\nWARNING!!! Size must be greater then 2.\n")
                else:
                    return i
            except ValueError as err:
                print(err)
                

    def buildField(self, field, size):
        """Outputs the current situation on the playing field to the console
        """
        #Prints first line
        pr_line = "  "
        for number in range(1, size+1):
            pr_line += " " + str(number)
        print(pr_line, "\n")
        #Prints other lines
        for lino, line in enumerate(field, 1):
            pr_line = " " + str(lino)
            for element in line:
                pr_line += " " + element
            print(pr_line, "\n")

    def updateCurrentSituation(self):
        size, flag_end, flag_draw, active_player, field = self.__model.getData()
        print("\n Current situation:")
        self.buildField(field, size)
        #Checks if the game has ended
        if flag_end:
            print("\n THE GAME END. \n WINNER: ", active_player)
        #Checks if the draw has happenned 
        elif flag_draw:
            print("\n THE GAME ENDED IN A DRAW")
        else:
            x, y = None, None
            while True:
                try:
                    #Queries the coordinates from the user (active player)
                    msg = active_player + " (coordinate: x y):"
                    line = input(msg)
                    if not line:
                        print("\nWarning!!! You  must enter the coordinate. ", 
                                                    "Example: 1 2")
                    else:
                        #Deletes last and first spaces
                        line = line.strip()
                        #Removes duplicate spaces
                        line_next = line.replace("  ", " ")
                        while line_next != line:
                            line = line_next
                            line_next = line.replace("  ", " ")
                        line = line_next
                        #Checks for the number of coordinates
                        if line.count(" ") > 1:
                            print("\nWarning!!! Should be only two ",
                                                        "coordinates: x y\n")
                        else:
                            #Separates coordinate values on different lines
                            x, y = line.split(" ")
                            #Translates str into int
                            x = int(x)
                            y = int(y)
                            #Checks values of coordinates
                            if ((x > size) or (y > size)):
                                print("\nWarning!!! Coordinate value should not",
                                    " be greater than the size of the field\n")
                            elif field[x-1][y-1] != " ":
                                print("\nWarning!!! Cell must be empty\n")
                            else:
                                break
                except ValueError as err:
                    print(err)
            if (x is not None) and (y is not None):
                self.__controller.setCell(x-1, y-1)
            else:
                print("!!!Error!!!")

#*****************************************************************************
#*****************************  CONTROLLER  **********************************
#*****************************************************************************

class TTTControllerInterface(metaclass=abc.ABCMeta):

    """ Class is the interface controller of the MVC pattern. It declares the
    basic methods that must be overridden by subclasses of controllers.
    """

    @abc.abstractmethod
    def __init__(self, model):
        pass

    @abc.abstractmethod
    def startWithStandartSize(self, size):
        pass

    @abc.abstractmethod
    def setCell(self, x, y):
        pass

class TTTController(TTTControllerInterface):
    """Controller (MVC). It implements the interaction between the view and
    the model. Controls operations model depending on user actions.
    """

    def __init__(self, model):
        self.__model = model
        self.__view = TTTView(self, model)
        self.__view.printStartMessage()

    
    def startWithStandartSize(self):
        """Starts the game with default settings
        """
        self.__model.startPlay()

    def startWithNoStandartSize(self):
        """Starts the game with non default settings
        """
        new_size =self.__view.queryChangeSize()
        self.__model.size = new_size
        self.__model.startPlay()

    def setCell(self, x, y):
        """Sets the next cell in model
        """
        self.__model.setCell(x, y)

main()
# if __name__ == "__main__":
    # import doctest
    # doctest.testmod()