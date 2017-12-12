#imports
from tkinter import *
from MineSweeperLogic import *
import random

"""This class acts as an interface for the user to interact with the
MinesweeperLogic class. It receives mouse information from the user and outputs
visual information in a tkinter window which is what the user would say is the
actual minesweeper game"""
class MineSweeperGUI(Canvas):

  CELL_SIZE = 30
  #This function initializes the tkinter canvas and all of the variables
  #used in minesweeper. The only thing parameters it receives are width height
  #and number of mines, all other variables are set to standard values and then
  #are changed accorsingly through the life of the game
  def __init__(self, canvas, width, height, numMines):
    size = MineSweeperGUI.CELL_SIZE
    Canvas.__init__(self, canvas, width = size*width, height = size*height)
    canvas.title("MineSweeper")
    self.canvas = canvas
    self.width = width
    self.height = height
    self.gameStarted = False
    self.gameEnded = False
    self.win = False
    self.grid = MineSweeperLogic(width,height,numMines)
    self.drawGrid()
    
    self.pressed = {}
    self.bind("<Button-1>",self.mousePress)
    self.bind("<B1-Motion>", self.mouseMove)
    self.bind("<Button-3>", self.rightClick)
    self.bind("<ButtonRelease-1>", self.mouseRelease)

  #This function does not explicitly draw the grid but rather goes through every
  #cell within the grid and draws them.
  def drawGrid(self):
    opened = self.grid.getOpen()
    num = self.grid.getNumAdj()
    for i in range(0,self.width):
      for j in range(0,self.height):
        self.drawCell(i,j,opened[i][j],num[i][j])

  #This function receives an array of opened values and then calls the drawCell
  #function for each of the values in the array. It receives an array so that
  #it can draw the least number of cells possible because the more cells that
  #have to be drawn the slower the program runs.
  def drawOpened(self,openedValues):
    opened = self.grid.getOpen()
    num = self.grid.getNumAdj()   
    for cell in range(0,len(openedValues)):
      x = openedValues[cell]["x"]
      y = openedValues[cell]["y"]
      self.drawCell(x,y,opened[x][y],num[x][y])

  #This function receives the x and y coordinates of a cell then draws it
  #depending on whether or not the cell is opened. If the cell is opened
  #it also needs the parameter which describes the number of adjacent mines.
  #If the number of adjacent mines is zero then it does not draw a number at all
  def drawCell(self,x,y,opened,*num):
    EDGE_SIZE = 15
    NUMBER_SCALE = 5
    size = MineSweeperGUI.CELL_SIZE
    xmin = x*size
    xmax = (x+1)*size
    ymin = y*size
    ymax = (y+1)*size
    diff = size/EDGE_SIZE
    font = 'TkDefaultFont'
    textSize = int(size-NUMBER_SCALE*diff)
    textX = xmin+size/2
    textY = ymin+size/2
    if opened:
      numStr = str(num[0])      
      fill = "#e0ecff"
      outline = "black"               
      self.create_rectangle(xmin, ymin, xmax,\
                                   ymax, fill = fill, outline = outline)
      if not num[0] == 0:
        self.create_text([textX,textY],text = numStr, font = (font,textSize))
      
    else:
      flagged = self.grid.getFlagged()
      if not flagged[x][y]:
        fill_0 = "white"
        fill_1 = "black"
        fill_2 = "grey"
        self.create_rectangle(xmin, ymin, xmax, ymax, fill = fill_0,width = 0)
        self.create_polygon([xmax,ymin,xmax,ymax,xmin,ymax], fill = fill_1)
        self.create_rectangle(xmin+diff,ymin+diff,xmax-diff,ymax-diff,fill=fill_2,width = 0)

  #This function draws the cell that is being pressed at that moment. It only
  #draws it if it is nor flagged. It is similar to a cell that has not been
  #opened however the colors and design are slightly different.
  def drawPressed(self,x,y):
    flagged = self.grid.getFlagged()
    if not flagged[x][y]:
      EDGE_SIZE = 15
      size = MineSweeperGUI.CELL_SIZE
      xmin = x*size
      xmax = (x+1)*size
      ymin = y*size
      ymax = (y+1)*size
      diff = size/EDGE_SIZE
      fill_0 = "white"
      fill_1 = "grey"
      fill_2 = "#cbd1db"
      self.create_rectangle(xmin, ymin, xmax, ymax, fill = fill_0,width = 0)
      self.create_polygon([xmax,ymin,xmax,ymax,xmin,ymax], fill = fill_1)
      self.create_rectangle(xmin+diff,ymin+diff,xmax-diff,ymax-diff,fill=fill_2,width = 0)

  #This funcion draws a cell that has been flagged. It receives the x and y
  #coordinates of the flagged cell.
  def drawFlag(self,x,y):
    size = MineSweeperGUI.CELL_SIZE
    xmin = x*size
    xmax = (x+1)*size
    ymin = y*size
    ymax = (y+1)*size
    diff = size/15
    fill_0 = "white"
    fill_1 = "grey"
    fill_2 = "#cbd1db"
    fill_3 = "red"
    self.create_rectangle(xmin, ymin, xmax, ymax, fill = fill_0,width = 0)
    self.create_polygon([xmax,ymin,xmax,ymax,xmin,ymax], fill = fill_1)
    self.create_rectangle(xmin+diff,ymin+diff,xmax-diff,ymax-diff,fill=fill_2,width = 0)
    self.create_polygon([xmax-diff,ymin+diff,xmax-diff,ymax-diff,xmin+diff,ymax-diff], fill = fill_3)

          
  #This function goes through each cell and draws a mine depending on whether
  #or not the cell holds a mine. This function is called at the end of the game
  #to tell the user which cells held mines. This function is only called if the
  #user "loses" or clicks a mine.
  def drawEndGame(self):
    mines = self.grid.getMines()
    for i in range(0,self.width):
      for j in range(0,self.height):
        if mines[i][j]:
          size = MineSweeperGUI.CELL_SIZE
          xmin = i*size
          xmax = (i+1)*size
          ymin = j*size
          ymax = (j+1)*size
          diff = size/6
          fill_0 = "red"
          fill_1 = "black"
          self.create_rectangle(xmin,ymin,xmax,ymax,fill=fill_0,outline=fill_1)
          self.create_rectangle(xmin+diff,ymin+diff,xmax-diff,ymax-diff,\
                                fill=fill_1,outline=fill_0)

  #This function creates a new tkinter window which receives a end game message
  #as a parameter. It creates a new endGame object
  def endGame(self):
    if self.win:
      message = "You Win!"
    else:
      message = "You lost."
    app = Tk()
    restart_window = MineSweeperEndGame(app,self.canvas,message)
    app.mainloop()
    
  #This function receives a mouse event and returns the coordinates of the event  
  def _eventCoords(self, event):
    size = MineSweeperGUI.CELL_SIZE
    y = int(event.y / size)
    x = int(event.x / size)
    return x,y

  #This function handles when the user right clicks. If the cell is not opened
  #and the game is not ended then this flags the cell and then draws the flag.
  #If the cell is flagged and the user right clicks it then it unflags the cell
  #and draws the unflagged cell in its place.
  def rightClick(self,event):
    if not self.gameEnded:
      opened = self.grid.getOpen()
      x,y = self._eventCoords(event)
      if not opened[x][y]:
        if self.grid.setFlag(x,y):
          self.drawFlag(x,y)
        else:
          self.drawCell(x,y,opened[x][y])

  #This is the function which handles when the user presses their mouse. It
  #calls the drawPressed function
  def mousePress(self,event):
    if not self.gameEnded:
      x,y = self._eventCoords(event)
      self.pressed["x"] = x
      self.pressed["y"] = y
      opened = self.grid.getOpen()
      cellStatus = opened[self.pressed["x"]][self.pressed["y"]]
      
      if not cellStatus:
        self.drawPressed(self.pressed["x"],self.pressed["y"])

  #This function is similar to the mousePress function however it has to handle
  #much more. It makes sure that the mouse is within the plane, and if the
  #user changes cell then it has to "unpress" the pressed cell and then press
  #the cell which the user is actually pressing.
  def mouseMove(self, event):
    if not self.gameEnded:
      x,y = self._eventCoords(event)
      opened = self.grid.getOpen()
      flagged = self.grid.getFlagged()
      num = self.grid.getNumAdj()
      if not (x == self.pressed["x"] and y == self.pressed["y"]):
        if x >= 0 and y >= 0 and\
           x < self.width and y < self.height:
          if not flagged[x][y]:
            cellStatus = opened[self.pressed["x"]][self.pressed["y"]]
            if not cellStatus:
              self.drawCell(self.pressed["x"],self.pressed["y"],cellStatus)
            self.pressed["x"] = x
            self.pressed["y"] = y
            cellStatus = opened[self.pressed["x"]][self.pressed["y"]]
            if not cellStatus:
              self.drawPressed(self.pressed["x"],self.pressed["y"])

  #This function handles when the mouse is released. It starts the game if the
  #game has not already been started, it calls for adjacent cells to be opened,
  #it makes sure the game is not ended, it checks to see if the user wins or loses
  #and it does nothing if the cell which the user releases their mouse on is flagged
  #or opened.
  def mouseRelease(self,event):
    if not self.gameEnded:
      x = self.pressed["x"]
      y = self.pressed["y"]
      flagged = self.grid.getFlagged()
      if not flagged[x][y]:
        opened = self.grid.getOpen()
        num = self.grid.getNumAdj()
        mines = self.grid.getMines()
        cellStatus = opened[x][y]
        mineStatus = mines[x][y]
        if not cellStatus:
          if not self.gameStarted:
            self.gameStarted = not self.gameStarted
            self.grid.startGame(x,y)
            openedValues = self.grid.openAdj(x,y)
            self.drawOpened(openedValues)
          else:
            if mineStatus:
              self.gameEnded = not self.gameEnded
              self.drawEndGame()
              self.endGame()
            else:
              openedValues = self.grid.openAdj(x,y)
              self.drawOpened(openedValues)
              self.win = self.grid.checkWin()
              if self.win:
                self.gameEnded = not self.gameEnded
                self.endGame()
"""This class is called when the game is ended. It is used to see if the user
wants to play again or quit. It is a GUI class in that it opens a GUI window."""
class MineSweeperEndGame():
  #This function receives the tkinter canvas which it is being drawn on and the
  #former minesweeper game's canvas as parameters as well as a message
  #depending on whether the user won or lost
  def __init__(self,canvas,mineCanvas,message):
    self.canvas = canvas
    self.mineCanvas = mineCanvas
    canvas.title("Game Finished")
    self.mainPrompt = Label(canvas,text=message).pack(side='top')
    self.newGame = Button(canvas,text = "New Game",command = self.newGame).pack(side='top')
    self.close = Button(canvas,text = "Close",command = self.close).pack(side='top')
  #If the user presses the close button, this function is called and it closes
  #itself and the former minesweeper game.
  def close(self):
    self.canvas.destroy()
    self.mineCanvas.destroy()
  #If the user presses newGame button this creates a runMineSweeper object and
  #then destroys itself and the previous minesweeper game.
  def newGame(self):
    mineCanvas = Tk()
    self.mineSweeperGame = runMineSweeper(mineCanvas)
    self.canvas.destroy()
    self.mineCanvas.destroy()
    mineCanvas.mainloop() 
"""This class is an options window which pops up before minesweeper is played.
It has three sizes and three difficulty levels, all which are preset as global
constants. The difficulty level is defined as the percentage of total cells that
are mines. When difficulty level and size have been chosen and the user presses
start the window is destroyed and a new window pops up with the minesweeper game"""
class runMineSweeper():
  DIFF = {"Easy":.10,"Medium":.15,"Hard":.25}
  SIZE = {"Small":{"x":10,"y":10},"Medium":{"x":20,"y":15},"Large":{"x":30,"y":20}}
  #This function creates a window with the options for minesweeper.
  #It is full of buttons that set the options when pressed.
  def __init__(self,canvas):
    self.canvas = canvas
    self.diff = "Medium"
    self.size = "Medium"
    canvas.title("MineSweeperOptions")
    self.diffFrame = Frame(canvas)
    self.diffFrame.pack(side = LEFT)
    self.sizeFrame = Frame(canvas)
    self.sizeFrame.pack(side = LEFT)
    self.startFrame = Frame(canvas)
    self.startFrame.pack(side = LEFT)
    self.mainPrompt = Label(self.diffFrame,text="Select Difficulty").pack(side='top')
    self.easyDiff = Button(self.diffFrame,text= "Easy",command=self.setDiffEasy,fg="white",bg='green').pack(side='top')
    self.medDiff = Button(self.diffFrame,text= "Medium",command=self.setDiffMed,fg="black",bg='yellow').pack(side='top')
    self.hardDiff = Button(self.diffFrame,text= "Hard",command=self.setDiffHard,fg="white",bg='red').pack(side='top')
    self.mainPrompt = Label(self.sizeFrame,text="Select Size").pack(side='top')
    self.smallSize = Button(self.sizeFrame,text= "Small",command=self.setSizeSmall,fg="white",bg='green').pack(side='top')
    self.medSize = Button(self.sizeFrame,text= "Medium",command=self.setSizeMed,fg="black",bg='yellow').pack(side='top')
    self.largeSize = Button(self.sizeFrame,text= "Large",command=self.setSizeLarge,fg="white",bg='red').pack(side='top')
    self.mainPrompt = Label(self.startFrame,text="Click to Start").pack(side='top')
    self.startButton = Button(self.startFrame,text= "Start",command=self.startMineSweeper).pack(side='top')

  #This function creates a MineSweeperLogic object and then opens a new window.
  #It then destroys itself.
  def startMineSweeper(self):
    width = runMineSweeper.SIZE[self.size]["x"]
    height = runMineSweeper.SIZE[self.size]["y"]
    mines = int(width*height*runMineSweeper.DIFF[self.diff])
    mineCanvas = Tk()
    mineCanvas.resizable(width=False,height=False)
    game = MineSweeperGUI(mineCanvas,width,height,mines)
    game.pack()
    self.canvas.destroy()
    mineCanvas.mainloop()

  #This function is called to set the difficulty to easy 
  def setDiffEasy(self):
    self.diff = "Easy"

  #This function is called to set the difficulty to medium
  def setDiffMed(self):
    self.diff = "Medium"

  #This function is called to set the difficulty to hard
  def setDiffHard(self):
    self.diff = "Hard"

  #This function is called to set the size to small
  def setSizeSmall(self):
    self.size = "Small"

  #This function is called to set the size to  medium
  def setSizeMed(self):
    self.size = "Medium"

  #This function is called to set the size to large
  def setSizeLarge(self):
    self.size = "Large"


    
