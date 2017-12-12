"""Grid class provides a template for data systems which implement grid
structures where the individual cells within the grid contain information
individual to the cell."""
class Grid:

  #init Provides a default set of traits to each cell in the grid provided by
  #the user. The grid is a two dimensional array and each cell is a dicionary
  #where the key is the trait and the value is the state of the trait.
  #x and y provide the dimensions of the grid and trait is a default
  #dictionary which is assigned to each cell
  def __init__(self,x,y,traits):
    self.__width = x
    self.__height = y
    self.__grid = []
    self.__traits = traits.keys()  
    for i in range(0,x):
      self.__grid.append([])
      for j in range(0,y):
        self.__grid[i].append(traits.copy())
        
  #Sets a value to a trait within a cell given the dimensions of the cell on
  #the grid (x and y) and the trait and corresponding value to be assigned
  #to the cell
  def setValue(self,x,y,trait,value):
    self.__grid[x][y][trait] = value

  #The below function returns a value given a trait 
  def getValue(self,x,y,trait):
    return self.__grid[x][y][trait]
  
  #This function returns a two dimentional array which is the size of the grid
  #and is populated with the states of a trait for each cell
  def getTraitArray(self,trait):
    traitArray = []
    for i in range(0,self.__width):
      traitArray.append([])
      for j in range(0,self.__height):
        traitArray[i].append(self.getValue(i,j,trait))
    return traitArray
  
  #This function takes in an array of traits and updates a each cell's
  #trait according to the inputted array, similar to getTraitArray except it
  #updates the traits given an array rather than getting an array
  def updateTraitArray(self,trait,traitArray):
    for i in range(0,self.__width):
      for j in range(0,self.__height):
        self.setValue(i,j,trait,traitArray[i][j])
        
  #This function receives the coordinates of a cell, a trait and a value, and
  #returns how many out of the eight adjacent cells have the trait at state
  #value. The wrap parameter is used to distinguish how the cells at the edge
  #of the grid handle adjacent cells. If wrap is True then the adjacent values
  #which go off the grid wrap around and detect the cell on the opposite edge
  #of the map. This creates continuous taurus shaped plane. If wrap is false
  #then the cell at the edge of the map does not count the values that extend
  #beyond the grid. If wrap is left as no value or False then it is considered
  #as False. Otherwise wrap is True.
  def getNumAdj(self,x,y,trait,value,*wrap):
    #Local Constant
    ADJ_VALS = [[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[-1,1],[0,1],[1,1]]
    counter = 0
    for i in range(0,len(ADJ_VALS)):
      xVal = x+ADJ_VALS[i][0]
      yVal = y+ADJ_VALS[i][1]
      if wrap and wrap[0]:
        if xVal == self.__width:
          xVal = 0
        if yVal == self.__height:
          yVal = 0
        if self.getValue(xVal,yVal,trait) == value:
          counter += 1
      else:
        if not (xVal == self.__width or xVal < 0 or\
                yVal == self.__height or yVal < 0) and \
                self.getValue(xVal,yVal,trait) == value:
          counter += 1
    return counter
  #This function returns the number of cells that hold a specific value for a
  #given trait. The trait and values are the parameters for the funciton.
  def getNumValue(self,trait,value):
    counter = 0
    for i in range(0,self.__width):
      for j in range(0,self.height):
        if self.getValue(i,j,trait) == value:
          counter += 1
    return counter
  def __str__(self):
    return "Grid size is: "+str(self.__width)+" by "+str(self.__height)+\
           ", traits are: "+", ".join(list(map(str,self.__traits)))
