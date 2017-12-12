#imports
from tkinter import*
from ConwaysLogic import*
import time, sched

"""The purpose of this class is to act as an interface for the user to act with
the ConwaysLogic class. This provides a visual output to the user and handles
all user input, then commumicates with the conways logic class to make the
program run."""
class ConwaysGUI(Canvas):
  #Constants
  CELL_SIZE = 10
  WIDTH = 100
  HEIGHT = 50
  #Creates ConwaysLogic object and sets up the tkinter window which
  #the user is interacting with.
  def __init__(self,canvas):
    self.size = ConwaysGUI.CELL_SIZE
    self.width = ConwaysGUI.WIDTH
    self.height = ConwaysGUI.HEIGHT
    Canvas.__init__(self, canvas, width = self.size*self.width,\
                    height = self.size*self.height)
    canvas.title("Conways Game of Life")
    self.playing = False
    self.grid = ConwaysLogic(self.width,self.height)
    self.drawGrid()
    
    self.bind("<Button-3>",self.switchGameplay)
    self.bind("<Button-1>",self.mousePress)
    self.bind("<B1-Motion>", self.mouseMove)
  #function to draw the grid, i and j are coordinates of the cell which
  #is to be drawn. This does not explicitly draw the grid but rather
  #calls the drawCell function for each cell within the grid.
  def drawGrid(self):
    for i in range(0,self.width):
      for j in range(0,self.height):
        if not self.grid.getValue(i,j):
          fill = "#e0ecff"
        else:
          fill = "black"        
        self.drawCell(i,j,fill)
  #Draws a cell based on the x and y coordinates and the fill which it
  #receives as a parameter
  def drawCell(self,x,y,fill):
    xmin = x*self.size
    xmax = (x+1)*self.size
    ymin = y*self.size
    ymax = (y+1)*self.size
    outline = "black"               
    self.create_rectangle(xmin, ymin, xmax,\
                          ymax, fill = fill, outline = outline)
  #Receives a mouse event and returns the coordinates of the event
  def _eventCoords(self, event):
    y = int(event.y / self.size)
    x = int(event.x / self.size)
    return x,y
  #Function which handles when the user presses the mouse. Changes the value
  #of the cell which is pressed to not what it was before. (False becomes True,
  #vice versa). Also calls the drawCell function for the cell which was clicked
  def mousePress(self,event):
    x,y = self._eventCoords(event)
    if not self.playing:
      value = self.grid.changeValue(x,y)
      if not value:
        fill = "#e0ecff"
      else:
        fill = "black"      
      self.drawCell(x,y,fill)

  #When the user glides there mouse over cells this function changes there
  #values to True then draws the cells whose values have been changes to True.
  #This function also checks to make sure that the mouse event is within the
  #boundaries of the grid to avoid errors.
  def mouseMove(self,event):
    x,y = self._eventCoords(event)
    if not self.playing:
      if x >= 0 and y >= 0 and\
         x < self.width and y < self.height:
        if not self.grid.getValue(x,y):
          self.grid.changeValue(x,y)
          fill = "black"      
          self.drawCell(x,y,fill)

  #This function handles when the user right clicks. It updates the board by
  #calling the update function.
  def switchGameplay(self,event):
    self.update()
  
  #This fucntion updates the board. It calls the ConwaysLogic updateBoard
  #function then receives an array of the cells which have had their values
  #changed so that it can re-draw them instead of re-drawing the whole board
  #which is slow and requires more graphics power than drawing the individual
  #cells.
  def update(self):
    updateBoard = self.grid.updateBoard()
    for i in range(0,len(updateBoard)):
      x = updateBoard[i]["x"]
      y = updateBoard[i]["y"]
      if not self.grid.getValue(x,y):
        fill = "#e0ecff"
      else:
        fill = "black"         
      self.drawCell(x,y,fill)
