import random
import time
from tkinter import *

DEFAULT_MULTIPLAYER = False
DEFAULT_HEIGHT = 10
DEFAULT_WIDTH = 10
DEFAULT_SIZE = 15
RESOLUTION = "800" + "x" + "630"
MAX_SIZE = 150
MAX_MAZE_SIDE = 300

# Map draw kommentointi

# TODO manual
# TODO resoluutio
# TODO save


class Maze_game:
    """
    Requires Class Cell to be defined to function properly.
    Labyrinth game. Take DEFAULT_SIZE, DEFAULT_WIDTH, and
    DEFAULT_HEIGHT and DEFAULT_MULTIPLAYER from Public variables
    """

    def __init__(self):
        self.__master = Tk()

        self.initUI()
        self.__master.iconbitmap(r"icon1.ico")
        self.__size = DEFAULT_SIZE
        self.__multiplayer = DEFAULT_MULTIPLAYER
        self.loop()

    def loop(self):
        """
        Loops the mainwindow (where maze is in)
        :return: None
        """

        # We want to start game without user needing to press start
        self.restart_game()

        while True:
            # Two loops cause we want to use different method for binding
            # depending on situation. Two methods with binding at the same
            # time didn't work either at tests.
            while self.__multiplayer is False:
                try:
                    self.__master.bind("<KeyPress>", self.move_player1)

                    # Is here to stablize
                    time.sleep(0.01)

                    # Unfortunately no grid plan or any object placement plan
                    # is available

                    self.__master.update_idletasks()
                    self.__master.update()

                # Is here so gives no error when exit by clicking "x"
                except TclError:
                    return

            while self.__multiplayer is True:
                try:
                    self.__master.update_idletasks()
                    self.__master.bind("<KeyPress>", self.move_both_players)
                    # Is here to stablize
                    time.sleep(0.01)
                    self.__master.update()

                # Is here so gives no error when exit by clicking "x"
                except TclError:
                    return

    def create_map(self):
        """
        Save  to each cell how it is connected. Most connection at one cell is 4
        (Up, left, down, right)
        :return: none
        """
        self.__cell_dict = {}

        self.__width = self.__size_check_width.get()
        self.__height = self.__size_check_height.get()

        # Create a list including cells and each cell name is format x"x
        # coordinate"y"y_coordinate" Where "x coordinate" and "y coordinate"
        # replaced with corresponding value
        for x in range(self.__width):
            for y in range(self.__height):
                self.__cell_dict[nimi(x, y)] = Cell(x, y, self.__width, self.__height)

        # save cell_dict to each cell
        for cell in self.__cell_dict:
            self.__cell_dict[cell].save(self.__cell_dict)

        # Choose a random cell and start making maze from there
        start_point_cell = self.__cell_dict[
            nimi(
                random.randint(0, self.__width - 1),
                (random.randint(0, self.__height - 1)),
            )
        ]
        start_point_cell.maze_maker_call(start_point_cell)

    def construct_map(self):
        """
        Construct a map according checking if which cells are connected together
        Save data to self.__xxx where True means connection to the cell  at right
        and to self.__yyy where True means connection tto the cell at down
        :return: none
        """

        self.__xxx = []
        y = 0
        # Safe every rows information how cells are connected vertically

        # Check every row is checked
        while y < self.__height:
            xx = [False]

            # Last row needs no checking as it would give no more information
            for x in range(self.__width):
                cell_name = nimi(x, y)

                if x < self.__width - 1:
                    # Check if current cell is connected to cell right to it
                    if (
                        self.__cell_dict[cell_name].return_neighbours()[nimi(x + 1, y)]
                        == xx[x]
                    ):
                        xx.append(xx[x])
                    else:
                        xx.append(not xx[x])
                # Creates border
                else:
                    xx.append(False)

            y += 1
            self.__xxx.append(xx)

        self.__yyy = []
        x = 0
        # Safe every columns information how cells are connected horizontally

        # Check every columns are checked
        while x < self.__width:
            yy = [False]

            # Last row needs no checking as it would give no more information
            for y in range(self.__height):
                cell_name = nimi(x, y)

                if y < self.__height - 1:
                    # Check if current cell is connected to cell down to it
                    if (
                        self.__cell_dict[cell_name].return_neighbours()[nimi(x, y + 1)]
                        == yy[y]
                    ):
                        yy.append(yy[y])
                    else:
                        yy.append(not yy[y])

                else:
                    # Creates border
                    yy.append(False)
            x += 1
            self.__yyy.append(yy)

        # Creates a starting point and an exit
        self.__yyy[0][0] = True
        self.__yyy[self.__width - 1][self.__height] = True

    def restart_game(self):
        """
        Initialize the game by calling all necessary functions for game to start
         as well as set values according how user wants to.
        :return: None
        """
        self.__label.config(text="Let the game on!")
        self.__game_on = True
        self.multiplayer_get()
        self.create_map()
        self.construct_map()

        # Clear the canvases
        self.__player1_canvas.delete("all")
        self.__player2_canvas.delete("all")

        # Draw player1 and his maze
        self.map_draw(self.__player1_canvas, "blue")

        # cords of player1 as [y,x]
        self.__player1_pos = [0, 1]

        if self.__multiplayer is True:
            self.__game_on_1 = True

            # Give both players equally screen space
            self.__player1_canvas.configure(width=300, height=600)
            self.__player2_canvas.configure(width=300, height=600)

            # Draw player2 and his maze
            self.map_draw(self.__player2_canvas, "red")

            # cords of player2 as [y,x]
            self.__player2_pos = [0, 1]
            self.__label2.grid()
            self.__label2.config(text="Let the game on!")

        else:
            # Set player1 to get player2 canva's space
            self.__player1_canvas.configure(width=600, height=600)
            self.__player2_canvas.configure(width=0, height=0)
            self.__label2.grid_remove()

    def exit_game(self):
        self.__master.destroy()

    def change_value(self, x):
        self.__size = int(x)

    def multiplayer_get(self):
        """
        Change self.__multiplayer value when tab is pressed
        :return: None
        """
        if self.__multiplayer_check.get() == 0:
            self.__multiplayer = False
        else:
            self.__multiplayer = True

    def validate_input(self, entry_input):
        """
        Check that entry_input is number(float or integer).
        Empty entry is also fine.

        :param entry_input: event
        :return: Boolean
        """
        if entry_input.isdigit():
            return True
        elif entry_input == "":
            return True
        else:
            return False

    def initUI(self):
        """
        Make all button and scales as well as player1_canvas(es) for playground(s).
        commands for buttons and scales and defined as methods.
        :return:
        """

        # self.__master includes player1_canvas, player2_canvas, labels and frame1 (everything)

        # frame1 includes frame2,frame3 and frame4 and buttons

        # frame2 includes entry1 and scale1 (width input)
        # frame3 includes entry2 and scale2 (height input)
        # frame4 included entry3 and scale3 (size input)

        self.__master.title("Path of Teekkari")

        self.__master.resizable(False, False)
        self.__master.geometry(RESOLUTION)

        # Save a validation callback to be used in entries
        register = self.__master.register(self.validate_input)

        self.__frame1 = Frame()

        self.__frame2 = Frame(self.__frame1)

        self.__entry1 = Entry(
            self.__frame2, width=3, validate="key", validatecommand=(register, "%P")
        )
        self.__entry1.bind("<Return>", self.update_values)
        self.__entry1.pack(side=LEFT, anchor=E, padx=10)

        self.__size_check_width = Scale(
            self.__frame2, length=100, from_=2, to=MAX_MAZE_SIDE, label="width"
        )
        self.__size_check_width.set(DEFAULT_WIDTH)
        self.__size_check_width.pack(anchor=W)

        self.__frame2.pack(anchor=W)

        self.__frame3 = Frame(self.__frame1)

        self.__entry2 = Entry(
            self.__frame3, width=3, validate="key", validatecommand=(register, "%P")
        )
        self.__entry2.bind("<Return>", self.update_values)
        self.__entry2.pack(side=LEFT, anchor=E, padx=10)

        self.__size_check_height = Scale(
            self.__frame3, length=100, from_=2, to=MAX_MAZE_SIDE, label="height"
        )
        self.__size_check_height.set(DEFAULT_HEIGHT)
        self.__size_check_height.pack(anchor=W)

        self.__frame3.pack(anchor=W)

        self.__frame4 = Frame(self.__frame1)

        self.__entry3 = Entry(
            self.__frame4, width=3, validate="key", validatecommand=(register, "%P")
        )
        self.__entry3.bind("<Return>", self.update_values)
        self.__entry3.pack(side=LEFT, anchor=E, padx=10)

        self.__size_check_size = Scale(
            self.__frame4,
            length=40,
            from_=5,
            to=MAX_SIZE,
            label="size",
            command=self.change_value,
        )
        self.__size_check_size.set(DEFAULT_SIZE)
        self.__size_check_size.pack(anchor=W)

        self.__frame4.pack(anchor=W)

        self.__exit_button = Button(
            self.__frame1,
            text="Exit game",
            borderwidth=2,
            relief=GROOVE,
            command=self.exit_game,
            width=10,
            height=1,
        )
        self.__exit_button.pack()

        self.__restart_button = Button(
            self.__frame1,
            text="Restart game",
            borderwidth=2,
            relief=GROOVE,
            command=self.restart_game,
        )
        self.__restart_button.pack()

        self.__multiplayer_check = IntVar()
        self.__multiplayer_button = Checkbutton(
            self.__frame1, text="Multiplayer", variable=self.__multiplayer_check
        )
        self.__multiplayer_button.pack()

        self.__player1_canvas = Canvas(self.__master)
        self.__player2_canvas = Canvas(self.__master)
        self.__player1_canvas.grid(row=0, column=0, columnspan=2)
        self.__player1_canvas.grid_propagate(True)
        self.__player2_canvas.grid(row=0, column=2, columnspan=2)
        self.__player2_canvas.grid_propagate(True)

        self.__label = Label(self.__master, text="moi")

        self.__label.grid(row=1, column=1, sticky=NW)
        self.__label2 = Label(self.__master, text="Let the game on")
        self.__label2.grid(row=1, column=3, sticky=NW)
        self.__frame1.grid(row=0, column=5, sticky=NE)

    def move_player1_canvas(self, x, y):
        self.__player1_canvas.move("all", x, y)

    def move_player2_canvas(self, x, y):
        self.__player2_canvas.move("all", x, y)

    def map_draw(self, player1_canvas, color):
        """
        Draw a maze(s) and player(s) using data saved to self.__xxx and self.__yyy
        If self.__multiplayer == True draw to identical mazes and inside of them
        different colored players
        :return: None
        """

        # Draw horizontal lines
        ycord = 0
        for x in self.__xxx:
            xcord = 0
            for boolean in x:
                # False in self.__xxx meant no connection with cell right to
                # so draws a line if so
                if boolean is False:
                    player1_canvas.create_line(
                        self.__size * (xcord + 1),
                        self.__size * (ycord + 1),
                        self.__size * (xcord + 1),
                        self.__size * (ycord + 2),
                    )
                xcord += 1
            ycord += 1
        xcord = 1

        # Draw vertical lines
        for y in self.__yyy:
            ycord = 1
            for boolean in y:
                if boolean is False:
                    # False in self.__xxx meant no connection with cell down to
                    # so draws a line if so
                    player1_canvas.create_line(
                        xcord * self.__size,
                        ycord * self.__size,
                        self.__size * (xcord + 1),
                        ycord * self.__size,
                    )
                ycord += 1
            xcord += 1

        # Create a movable object
        if color == "blue":
            self.__player1 = player1_canvas.create_rectangle(
                self.__size + 2,
                2,
                self.__size + self.__size - 2,
                self.__size - 2,
                fill=color,
            )
        else:
            self.__player2 = player1_canvas.create_rectangle(
                self.__size + 2,
                2,
                self.__size + self.__size - 2,
                self.__size - 2,
                fill=color,
            )

    def update_values(self, event):
        """
        Update every entrys to corresponding value (width,height and size)
        and clear all entries
        :param event:
        :return:
        """

        # TclError occurs when entry is empty.
        width = self.__entry1.get()
        try:
            self.__size_check_width.set(width)
        except TclError:
            pass
        height = self.__entry2.get()
        try:
            self.__size_check_height.set(height)
        except TclError:
            pass
        size = self.__entry3.get()
        try:
            self.__size_check_size.set(size)
        except TclError:
            pass

        # Get | mark out of entry
        self.__frame1.focus()

        self.__entry1.delete(0, "end")
        self.__entry2.delete(0, "end")
        self.__entry3.delete(0, "end")

    def move_player1(self, event):
        """
        Move player1 or his camera corresponding to event (KeyPress)
        Doesn't include both players moving because implementing cameras and so on
        would look more complicated.
        :param event:
        :return:
        """

        keypress = event.keysym.lower()

        # wasd player moving, tfgh camera moving
        if (
            keypress
            in {
                "a": "left",
                "w": "up",
                "s": "down",
                "d": "right",
                "t": "camera_up",
                "g": "camera_down",
                "h": "camera_right",
                "f": "camera_left",
            }
            and self.__game_on is True
        ):
            if self.__game_on is True:
                # move point view corresponding to key
                if keypress == "t":
                    self.move_player1_canvas(0, 300)
                elif keypress == "g":
                    self.move_player1_canvas(0, -300)
                elif keypress == "f":
                    self.move_player1_canvas(300, 0)
                elif keypress == "h":
                    self.move_player1_canvas(-300, 0)

                # Rest of methdod check if moving button is pressed
                # and if so move and modify player1 position as well
                elif keypress == "d":
                    if (
                        self.__xxx[self.__player1_pos[0] - 1][self.__player1_pos[1]] is True
                        and self.__player1_pos[0] != 0
                    ):
                        self.__player1_canvas.move(self.__player1, self.__size, 0)

                        self.__player1_pos[1] += 1

                elif keypress == "a":
                    if (
                        self.__xxx[self.__player1_pos[0] - 1][self.__player1_pos[1] - 1] is True
                    ):
                        self.__player1_canvas.move(self.__player1, -self.__size, 0)

                        self.__player1_pos[1] -= 1

                elif keypress == "s":
                    if (
                        self.__yyy[self.__player1_pos[1] - 1][self.__player1_pos[0]] is True
                    ):
                        self.__player1_canvas.move(self.__player1, 0, self.__size)

                        self.__player1_pos[0] += 1

                        if self.__player1_pos == [self.__height + 1, self.__width]:
                            self.__game_on = False
                            self.__label.config(text="Win!")

                elif keypress == "w":
                    if (
                        self.__yyy[self.__player1_pos[1] - 1][self.__player1_pos[0] - 1] is True
                    ):
                        self.__player1_canvas.move(self.__player1, 0, -self.__size)
                        self.__player1_pos[0] -= 1

    def move_both_players(self, event):
        """
        move either player or his camera according to given event (KeyPress)
        :param event:
        :return:
        """

        # wasd player1  moving, tfgh player1 camera moving
        # up,left,down,right player2 moving, ijkl player2 camera moving

        keypress = event.keysym.lower()

        # Player1 controls
        if (
            keypress
            in {
                "a": "left",
                "w": "up",
                "s": "down",
                "d": "right",
                "t": "camera_up",
                "g": "camera_down",
                "h": "camera_right",
                "f": "camera_left",
            }
            and self.__game_on is True
        ):
            # move player1 point view corresponding to key
            if keypress == "t":
                self.move_player1_canvas(0, 150)
            elif keypress == "g":
                self.move_player1_canvas(0, -150)
            elif keypress == "f":
                self.move_player1_canvas(150, 0)
            elif keypress == "h":
                self.move_player1_canvas(-150, 0)

            # Rest of this if check if moving button is pressed
            # to move player1 and if so move and modify player1 position as well
            elif keypress == "d":
                if (
                    self.__xxx[self.__player1_pos[0] - 1][self.__player1_pos[1]] is True
                    and self.__player1_pos[0] != 0
                ):
                    self.__player1_canvas.move(self.__player1, self.__size, 0)

                    self.__player1_pos[1] += 1

            elif keypress == "a":
                if (
                    self.__xxx[self.__player1_pos[0] - 1][self.__player1_pos[1] - 1] is True
                ):
                    self.__player1_canvas.move(self.__player1, -self.__size, 0)

                    self.__player1_pos[1] -= 1

            elif keypress == "s":
                if self.__yyy[self.__player1_pos[1] - 1][self.__player1_pos[0]] is True:
                    self.__player1_canvas.move(self.__player1, 0, self.__size)

                    self.__player1_pos[0] += 1

                    # Check if player1 found his way out of the maze
                    if self.__player1_pos == [self.__height + 1, self.__width]:
                        self.__game_on = False

                        # Chech if player1 is already finished
                        # and change label text
                        if self.__game_on_1 is True:
                            self.__label.config(text="Win!")
                        else:
                            self.__label.config(text="Finally, thank god!")

            elif keypress == "w":
                if (
                    self.__yyy[self.__player1_pos[1] - 1][self.__player1_pos[0] - 1] is True
                ):
                    self.__player1_canvas.move(self.__player1, 0, -self.__size)

                    self.__player1_pos[0] -= 1

        # Player2 controls
        elif (
            keypress
            in {
                "left": "left",
                "up": "up",
                "down": "down",
                "right": "right",
                "i": "camera up",
                "j": "camera left",
                "k": "camera down",
                "l": "camera right",
            }
            and self.__game_on_1 is True
        ):
            # move player2 point view corresponding to key
            if keypress == "i":
                self.move_player2_canvas(0, 150)
            elif keypress == "k":
                self.move_player2_canvas(0, -150)
            elif keypress == "j":
                self.move_player2_canvas(150, 0)
            elif keypress == "l":
                self.move_player2_canvas(-150, 0)

            # Rest of this if check if moving button is pressed
            # to move player2 and if so move and modify player1 position as well
            elif event.keysym == "Right":
                if (
                    self.__xxx[self.__player2_pos[0] - 1][self.__player2_pos[1]] is True
                    and self.__player2_pos[0] != 0
                ):
                    self.__player2_canvas.move(self.__player2, self.__size, 0)
                    self.__player2_pos[1] += 1

            elif event.keysym == "Left":
                if (
                    self.__xxx[self.__player2_pos[0] - 1][self.__player2_pos[1] - 1] is True
                ):
                    self.__player2_canvas.move(self.__player2, -self.__size, 0)
                    self.__player2_pos[1] -= 1

            elif event.keysym == "Down":
                if self.__yyy[self.__player2_pos[1] - 1][self.__player2_pos[0]] is True:
                    self.__player2_canvas.move(self.__player2, 0, self.__size)
                    self.__player2_pos[0] += 1

                    if self.__player2_pos == [self.__height + 1, self.__width]:
                        self.__game_on_1 = False

                        # Chech if player1 is already finished
                        # and change label text
                        if self.__game_on is True:
                            self.__label2.config(text="Win!")
                        else:
                            self.__label2.config(text="Finally, thank god!")

            elif event.keysym == "Up":
                if (
                    self.__yyy[self.__player2_pos[1] - 1][self.__player2_pos[0] - 1] is True
                ):
                    self.__player2_canvas.move(self.__player2, 0, -self.__size)
                    self.__player2_pos[0] -= 1


class Cell:
    """
    Core of map making. Is used by Maze_game
    :param x_cor int, y_cor int,width (of the maze) int, height(of the maze) int
    """

    def __init__(self, x_cor, y_cor, width, height):
        self.__x_cor = x_cor
        self.__y_cor = y_cor
        self.__neighbours = {}
        self.__width = width
        self.__height = height
        self.create_neighbours()
        self.__came_from = None
        self.__visited = False
        self.__cells_name = nimi((self.__x_cor), (self.__y_cor))

    def return_cells_name(self):
        """
        :return: str
        """
        return self.__cells_name

    def return_visited(self):
        """

        :return: boolean
        """
        return self.__visited

    def make_visited(self):
        self.__visited = True

    def return_neighbours(self):
        """
        :return: Dict, Contains all cell neighbours
        """
        return self.__neighbours

    def create_neighbours(self):
        """
        Create neighbours from all sided cells and defining there is a wall to separate them
        :return: None
        """
        if self.__x_cor != 0:
            # add neighbour to left side
            self.__neighbours[nimi((self.__x_cor - 1), (self.__y_cor))] = False
        if self.__x_cor != self.__width - 1:
            # add neighbour to right side
            self.__neighbours[nimi((self.__x_cor + 1), (self.__y_cor))] = False
        if self.__y_cor != 0:
            # add neighbour to up side
            self.__neighbours[nimi((self.__x_cor), (self.__y_cor - 1))] = False
        if self.__y_cor != self.__height - 1:
            # add neighbour to down side
            self.__neighbours[nimi((self.__x_cor), (self.__y_cor + 1))] = False

    def save(self, cell_dict):
        self.__cell_dict = cell_dict

    def maze_maker_call(self, neighbour):
        """
        This function was made to prevent recursion error while creating maze
        Just loop method maze_maker until it gives feedback to stop
        """

        test = True
        while test is True:
            test, neighbour = neighbour.maze_maker(self.__cell_dict)

    def maze_maker(self, cell_dict):
        """
        Choose a random neighbour that is not visited and move on there
        and also call breakwall between those two cells. Normally returns True
        and random neighbour from current cell. If all neighbours already
        visited returns neighbour it camed from. If it is the starting point returns False.
        :param cell_dict: dict
        :return:Boolean True if to be continued looping this method,
        Cell, Cell where we continue looping
        """

        naapuri_lista = []

        self.__visited = True

        # Check which neighbours status is visited is false, and add it to naapuri_lista
        for x in self.__neighbours:
            if self.__cell_dict[x].return_visited() is False:
                naapuri_lista.append(x)

        if not naapuri_lista == []:
            # Choose a random neighbour from naapuri_lista, make it visited,
            # call that neighbour to break wall with current cell and break wall
            # to neighbour as well. Then tell to continue maze making from the
            # random neighbour we got
            neighbours_name = random.choice(naapuri_lista)
            neighbour = self.__cell_dict[neighbours_name]
            neighbour.make_visited()
            self.__neighbours[(neighbours_name)] = True
            neighbour.break_wall(self.__cells_name)
            return True, neighbour

        # None means that creation is ready
        elif self.__came_from is not None:
            # In case all neighbours visited status is True go pack the cell
            # it came from and tell to continue there maze making
            return True, cell_dict[self.__came_from]

        else:
            # All Cells are now visited and tell to stop maze making
            return False, None

    def break_wall(self, neighbours_name):
        self.__neighbours[(neighbours_name)] = True
        self.__came_from = neighbours_name


def nimi(x, y):
    """
    Made to name Cells developer friendly way
    :param x: x-coordinate
    :param y: y-coordinate
    :return: str: x and y coordinate stringed
    """
    return "x" + str(x) + "y" + str(y)


def main():
    Maze_game()


main()
