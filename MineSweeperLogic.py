#imports
from Grid import*
import random

"""This class implements the logic for minesweeper which entails creation of the
board, detection of adjacent mines, and opening adjacent values upon click."""
class MineSweeperLogic:
  #constants
  TRAITS = {"AdjMines":0,"Mine":False,"Open":False,"Flag":False}
  NUM_EMPTY = 9
  
  #This fucntion receives width, height, and number of mines as parameters
  #then creates a grid object to handle the information. It also detects to
  #make sure the caling function has entered a valid number of mines, and
  #adjusts the number of mines accordingly.
  def __init__(self,width,height,numMines):
    self.__width = width
    self.__height = height
    if numMines > width*height-MineSweeperLogic.NUM_EMPTY:
      self.__numMines = width*height-MineSweeperLogic.NUM_EMPTY
    else:
      self.__numMines = numMines
    self.__board = Grid(width,height,MineSweeperLogic.TRAITS)

  #This fucntion starts the game by generating random mines and then for each
  #cell getting the number of adjacent mines that each cel has. X and Y are
  #parameters which desctibe the cell that the user has clicked to start the
  #game then those are passed into the generateMines function
  def startGame(self,x,y):
    self.generateMines(x,y)
    self.getNumAdjMines()

  #This function generates mines in random locations based on the first location
  #which the user has clicked. It uses a while loop to make sure that the number
  #of mines which have been placed matches self.__mines. It also checks to make
  #sure that a mine has not been placed where the user has clicked or in any
  #of the 8 adjacent cells which creates a starting point for the user to play
  #from
  def generateMines(self,x,y):
    minesLeft = self.__numMines
    while minesLeft > 0:
      mineX = random.randint(0,self.__width-1)
      mineY = random.randint(0,self.__height-1)
      if not (self.__board.getValue(mineX,mineY,"Mine") or\
              mineX == x and mineY == y):
        self.__board.setValue(mineX,mineY,"Mine",True)
        minesLeft -= 1
      if self.__board.getNumAdj(x,y,"Mine",True) > 0:
        self.__board.setValue(mineX,mineY,"Mine",False)
        minesLeft += 1

  #This function goes through every cell in the grid and finds how many mines
  #are adjacent to each respective cell. i and j are coordinates of the cell.
  #This uses the grid class's getNumAdj function to get how many adjacent mines
  #a cell has.
  def getNumAdjMines(self):
    for i in range(0,self.__width):
      for j in range(0,self.__height):
        numAdj = self.__board.getNumAdj(i,j,"Mine",True)
        self.__board.setValue(i,j,"AdjMines",numAdj)

  #This function receives an coordinate as x and y and the opens the adjacent
  #cells. It does so by checking the adjacent cells to see how many mines they
  #are adjacent to then opening them and adds them to an array for the same
  #process to be completed on them. It is an itterative solution to a recursive
  #problem. It also creates an array of the cells which have been opened and
  #returns it to the calling function so the calling function knows which cells
  #have been opened.
  def openAdj(self,x,y):
    openedCells = []
    self.__board.setValue(x,y,"Open",True)
    openedCells.append({"x":x,"y":y})
    if self.__board.getValue(x,y,"AdjMines") == 0:
      ADJ_VALS = [[-1,-1],[0,-1],[1,-1],[-1,0],[0,0],[1,0],[-1,1],[0,1],[1,1]]
      cellsToCheck = [{"x":x,"y":y}]
      for i in cellsToCheck:
        for j in range(0,len(ADJ_VALS)):
          xVal = i["x"] + ADJ_VALS[j][0]
          yVal = i["y"] + ADJ_VALS[j][1]
          if xVal >= 0 and xVal < self.__width and\
             yVal >= 0 and yVal < self.__height:
            if not self.__board.getValue(xVal,yVal,"Open") and\
               self.__board.getValue(xVal,yVal,"AdjMines") == 0 and\
               not self.__board.getValue(xVal,yVal,"Flag"):
              cellsToCheck.append({"x":xVal,"y":yVal})
            if not self.__board.getValue(xVal,yVal,"Mine") and\
               not self.__board.getValue(xVal,yVal,"Flag"):
              self.__board.setValue(xVal,yVal,"Open",True)
              openedCells.append({"x":xVal,"y":yVal})
    return openedCells

  #This function changes the flag value of a particular cell in position x,y
  #to not what it was before, then returns the value which it has been changed to
  def setFlag(self,x,y):
    flagValue = not self.__board.getValue(x,y,"Flag")
    self.__board.setValue(x,y,"Flag",flagValue)
    return flagValue

  #This function checks to see if the user has won. It does so by seeing if the
  #number of opened cells is equal to the size of the map minus the number of mines.
  def checkWin(self):
    return self.__numMines+self.getNumOpened() == self.__width*self.__height

  #This function goes through every cell and checks to see if it is opened.
  #If it is opened then it adds one to count. At the end it returns count,
  #the number of opened cells.
  def getNumOpened(self):
    count = 0
    opened = self.getOpen()
    for i in range(0,self.__width):
      for j in range(0,self.__height):
        if opened[i][j]:
          count += 1
    return count

  #This function utilizes the Grid class's getTraitArray function to return
  #an array with the current states of Mine for each cell.
  def getMines(self):
    return self.__board.getTraitArray("Mine")

  #This function utilizes the Grid class's getTraitArray function to return
  #an array with the current states of AdjMines for each cell.  
  def getNumAdj(self):
    return self.__board.getTraitArray("AdjMines")

  #This function utilizes the Grid class's getTraitArray function to return
  #an array with the current states of Open for each cell.
  def getOpen(self):
    return self.__board.getTraitArray("Open")

  #This function utilizes the Grid class's getTraitArray function to return
  #an array with the current states of Flagged for each cell.
  def getFlagged(self):
    return self.__board.getTraitArray("Flag")
