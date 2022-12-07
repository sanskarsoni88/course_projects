# Group#: G12
# Student Names: Cullen Jamieson, Sanskar Soni

import threading
import queue        #the thread-safe queue from Python standard library

from tkinter import Tk, Canvas, Button
import random, time

class Gui():
    """
        This class takes care of the game's graphic user interface (gui)
        creation and termination.
    """
    def __init__(self, queue, game):                                                                        
        """        
            The initializer instantiates the main window and 
            creates the starting icons for the snake and the prey,
            and displays the initial gamer score.
        """
        #some GUI constants
        scoreTextXLocation = 60
        scoreTextYLocation = 15
        textColour = "white"
        #instantiate and create gui
        self.root = Tk()
        self.canvas = Canvas(self.root, width = WINDOW_WIDTH, 
            height = WINDOW_HEIGHT, bg = BACKGROUND_COLOUR)
        self.canvas.pack()
        #create starting game icons for snake and the prey
        self.snakeIcon = self.canvas.create_line(
            (0, 0), (0, 0), fill=ICON_COLOUR, width=SNAKE_ICON_WIDTH)
        self.preyIcon = self.canvas.create_rectangle(
            0, 0, 0, 0, fill=ICON_COLOUR, outline=ICON_COLOUR)
        #display starting score of 0
        self.score = self.canvas.create_text(
            scoreTextXLocation, scoreTextYLocation, fill=textColour, 
            text='Your Score: 0', font=("Helvetica","11","bold"))
        #binding the arrow keys to be able to control the snake
        for key in ("Left", "Right", "Up", "Down"):
            self.root.bind(f"<Key-{key}>", game.whenAnArrowKeyIsPressed)

    def gameOver(self):
        """
            This method is used at the end to display a
            game over button.
        """
        gameOverButton = Button(self.canvas, text="Game Over!", 
            height = 3, width = 10, font=("Helvetica","14","bold"), 
            command=self.root.destroy)
        self.canvas.create_window(200, 100, anchor="nw", window=gameOverButton)
    

class QueueHandler():
    """
        This class implements the queue handler for the game.
    """
    def __init__(self, queue, gui):
        self.queue = queue
        self.gui = gui
        self.queueHandler()
    
    def queueHandler(self):
        '''
            This method handles the queue by constantly retrieving
            tasks from it and accordingly taking the corresponding
            action.
            A task could be: game_over, move, prey, score.
            Each item in the queue is a dictionary whose key is
            the task type (for example, "move") and its value is
            the corresponding task value.
            If the queue.empty exception happens, it schedules 
            to call itself after a short delay.
        '''
        try:
            while True:
                task = self.queue.get_nowait()
                if "game_over" in task:
                    gui.gameOver()
                elif "move" in task:
                    points = [x for point in task["move"] for x in point]
                    gui.canvas.coords(gui.snakeIcon, *points)
                elif "prey" in task:
                    gui.canvas.coords(gui.preyIcon, *task["prey"])
                elif "score" in task:
                    gui.canvas.itemconfigure(
                        gui.score, text=f"Your Score: {task['score']}")
                self.queue.task_done()
        except queue.Empty:
            gui.root.after(100, self.queueHandler)


class Game():
    '''
        This class implements most of the game functionalities.
    '''
    def __init__(self, queue):
        """
           This initializer sets the initial snake coordinate list, movement
           direction, and arranges for the first prey to be created.
        """
        self.queue = queue
        self.score = 0
        #starting length and location of the snake
        #note that it is a list of tuples, each being an
        # (x, y) tuple. Initially its size is 5 tuples.       
        self.snakeCoordinates = [(495, 55), (485, 55), (475, 55),
                                 (465, 55), (455, 55)]
        #prey's center coordinates stored as a field of Game (initially given an arbitrary number)
        self.preyCoordinates : list = [0,0]                                                         
        #initial direction of the snake
        self.direction = "Left"
        self.gameNotOver = True
        self.createNewPrey()     #immedeately changes self.preyCoordinates

    def superloop(self) -> None:
        """
            This method implements a main loop
            of the game. It constantly generates "move" 
            tasks to cause the constant movement of the snake.
            Use the SPEED constant to set how often the move tasks
            are generated.
        """
        SPEED = 0.15                        #seconds after which snake makes a move
        while self.gameNotOver:             #while snake is still alive
            time.sleep(SPEED)               #wait SPEED seconds before every move
            Move = {"move" : self.snakeCoordinates }   #create a Move dictionary with key "move".
            gameQueue.put(Move)                        #add task "move" to queue
            self.move()                                #call function to generate next move of snake

    def whenAnArrowKeyIsPressed(self, e) -> None:
        """ 
            This method is bound to the arrow keys
            and is called when one of those is clicked.
            It sets the movement direction based on 
            the key that was pressed by the gamer.
            Use as is.
        """
        currentDirection = self.direction
        #ignore invalid keys
        if (currentDirection == "Left" and e.keysym == "Right" or 
            currentDirection == "Right" and e.keysym == "Left" or
            currentDirection == "Up" and e.keysym == "Down" or
            currentDirection == "Down" and e.keysym == "Up"):
            return
        self.direction = e.keysym

    def move(self) -> None:
        """ 
            This method implements what is needed to be done
            for the movement of the snake.
            It generates a new snake coordinate. 
            If based on this new movement, the prey has been 
            captured, it adds a task to the queue for the updated
            score and also creates a new prey.
            It also calls a corresponding method to check if 
            the game should be over. 
            The snake coordinates list (representing its length 
            and position) should be correctly updated.
        """
        NewSnakeCoordinates = self.calculateNewCoordinates()     #gives the new coordinate to be added to the front of the snake as it moves
        #complete the method implementation below
        self.snakeCoordinates.append(NewSnakeCoordinates)        #add new coordinate to self.snakeCoordinates

        #values used later to check if prey has been eaten or not
        headX : int = NewSnakeCoordinates[0]           #x coordinate of the center of the head of the snake
        preyX : int = self.preyCoordinates[0]          #x coordinate of the center of the prey
        headY : int = NewSnakeCoordinates[1]           #y coordinate of the center of the head of the snake
        preyY : int = self.preyCoordinates[1]          #y coordinate of the center of the prey

        if -2.5 <= headX - preyX <= 2.5 and -2.5 <= headY - preyY <= 2.5:      #prey is eaten if both x and y of the center of the prey are within +/- 2.5 (2.5 included) of the center of the head of the snake
            self.score += 1                            #prey eaten so increase score
            Score = {"score" : self.score}             #create a dictionary with key "score" 
            gameQueue.put(Score)                       #add task "score" to queue
            self.createNewPrey()                       #new prey needs to be created
        else:
            self.snakeCoordinates = self.snakeCoordinates[1:]                  #prey not eaten so the first coordinate from the tail end of the snake needs to be removed from self.snakeCoordinates
            self.isGameOver(NewSnakeCoordinates)                               #check if game is over

    def calculateNewCoordinates(self) -> tuple:
        """
            This method calculates and returns the new 
            coordinates to be added to the snake
            coordinates list based on the movement
            direction and the current coordinate of 
            head of the snake.
            It is used by the move() method.    
        """
        lastX, lastY = self.snakeCoordinates[-1]       #lastX and lastY are the x and y coordinates of the center of the head of the snake respectively
        #complete the method implementation below
        #new variables created for readability
        newX : int = lastX                             #represents the new x coordinate of the head of the snake after move         
        newY : int = lastY                             #represents the new y coordinate of the head of the snake after move 

        spacing = 10 # Spacing between blocks

        #depending on the direction, head of the snake moves 10 units in that direction
        if self.direction == "Left":
            newX = lastX - spacing
        elif self.direction == "Right":
            newX = lastX + spacing
        elif self.direction == "Up":
            newY = lastY - spacing
        else:
            newY = lastY + spacing
        
        result = (newX, newY)
        return result      #return new coordinates of the head of the snake

    def isGameOver(self, snakeCoordinates) -> None:
        """
            This method checks if the game is over by 
            checking if now the snake has passed any wall
            or if it has bit itself.
            If that is the case, it updates the gameNotOver 
            field and also adds a "game_over" task to the queue. 
        """
        x, y = snakeCoordinates # Here, we are getting the coordinates of the snake head                                                                             
        #complete the method implementation below

        snakeBody: list = [] # List of coordinates not containing the head
        bitesItself : bool = False # Indicates whether or not the snake head coordinates match any coordinates from the body

        # Create the snake body (without head)
        for i in self.snakeCoordinates[:-1]: 
            snakeBody.append(i)

        # Check if the snake has bitten itself
        for i in snakeBody:
            if x == i[0] and y == i[1]:
                bitesItself = True

        # The game is over when: 
            # 1.) the snake head coordinates leave the game boundaries
            # 2.) the snake bites itself
        if x < 0 or x > WINDOW_WIDTH or y < 0 or y > WINDOW_HEIGHT or bitesItself == True:
            self.gameNotOver = False # Update the field
            game_over = {"game_over" : True} # Create the dictionary task with key "game_over"
            gameQueue.put(game_over) # Add the task to the queue


    def createNewPrey(self) -> None:
        """ 
            This methods picks an x and a y randomly as the coordinate 
            of the new prey and uses that to calculate the 
            coordinates (x - 5, y - 5, x + 5, y + 5). 
            It then adds a "prey" task to the queue with the calculated
            rectangle coordinates as its value. This is used by the 
            queue handler to represent the new prey.                    
            To make playing the game easier, set the x and y to be THRESHOLD
            away from the walls. 
        """
        THRESHOLD = 15 #sets how close prey can be to borders
        #complete the method implementation below

        #if x and y were completely random, the only way the snake can eat any prey is if the spacing used in calculateNewCoordinates is <= 6.
        #However, this makes the GUI very laggy and it looks different from the demo video.
        #So, instead, it was agreed upon to rather spawn prey only at x and y that can be reached by the snake.
        #This is so that the gamer has a better GUI.
        #This corresponds to x and y being both mutliples of 10 in their respective ranges along with a variability of +/- 2.

        #generate x and y within respective ranges that are multiples of 10 or the boundary values
        x = random.randrange(THRESHOLD, WINDOW_WIDTH - THRESHOLD, 10)
        y = random.randrange(THRESHOLD, WINDOW_HEIGHT - THRESHOLD, 10)

        #i and randomnessInteger are values used to increase randomness
        i : int = random.randint(0,2)       #value to be added/subtracted
        randomnessInteger : int  = random.randint(0,1)   #if 0, addition of i to x and y. if 1, subtraction of i
        
        if randomnessInteger == 0:
                x = x + i
                y = y + i
        elif x != 15 and y != 15:          # don't subtract if either are 15 as least value for x and y is THRESHOLD == 15
                x = x - i
                y = y - i

        self.preyCoordinates = [x, y]                           #update self.preyCoordinates
        rectangleCoordinates = (x - 5, y - 5, x + 5, y + 5)     #create rectangleCoordinates of the prey
        prey = {"prey" : rectangleCoordinates}                  #create dictionary task with key "prey"
        gameQueue.put(prey)                                     #add task to queue


if __name__ == "__main__":
    #some constants for our GUI
    WINDOW_WIDTH = 500           
    WINDOW_HEIGHT = 300 
    SNAKE_ICON_WIDTH = 15
    
    BACKGROUND_COLOUR = "green"   #you may change this colour if you wish
    ICON_COLOUR = "yellow"        #you may change this colour if you wish

    gameQueue = queue.Queue()     #instantiate a queue object using python's queue class

    game = Game(gameQueue)        #instantiate the game object

    gui = Gui(gameQueue, game)    #instantiate the game user interface
    
    QueueHandler(gameQueue, gui)  #instantiate our queue handler    
    
    #start a thread with the main loop of the game
    threading.Thread(target = game.superloop, daemon=True).start()

    #start the GUI's own event loop
    gui.root.mainloop()
