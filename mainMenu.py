from tkinter import *
from MineSweeperOutput import *
from ConwaysOutput import *

'''The main menu serves as the hub for both Mine Sweeper and Conway's Game of Life. From here, the user can select
which game they want to play.'''

class MainMenu:

  # Creates the main menu window, as well as the buttons that enable the user to play both games
  # canvas - takes in the window for the UI to be displayed
  def __init__(self,canvas):
    self.canvas = canvas
    self.canvas.title("Game Center")
    self.canvas.configure(bg='white')
    self.welcomeLabel = Label(self.canvas,text="Welcome to Game Center",bg="red",fg="white",font= ('arial',18)).pack(side='top',fill = BOTH)
    self.selectLabel = Label(self.canvas,text="Select a game to play:",bg='blue',fg='white',font = ('arial',14)).pack(side='top',fill = BOTH)
    self.mineSweeperButton = Button(self.canvas,text= "Mine Sweeper",command=self.runMineSweeper,bg='red',fg='white').pack(side='top')
    self.conwayButton = Button(self.canvas, text="Conway's Game of Life",command=self.runConways,bg="blue",fg='white').pack(side='top')
    self.closeButton = Button(self.canvas,text = 'Quit', command = self.closeWindow).pack(side = 'left')

  # Runs Mine Sweeper and displays it in a new window
  def runMineSweeper(self):
    mineCanvas = Tk()
    self.mineSweeperGame = runMineSweeper(mineCanvas)
    mineCanvas.mainloop()

  # Runs Conway's Game of Life and displays it in a new window
  def runConways(self):
    conwaysCanvas = Tk()
    conwaysCanvas.resizable(width=False,height=False)
    self.conwaysGame = ConwaysGUI(conwaysCanvas)
    self.conwaysGame.pack()
    conwaysCanvas.mainloop()

  # When quit button is pressed, the main menu window will close
  def closeWindow(self):
    self.canvas.destroy()

# Creates canvas, assigns menu to the MainMenu object, using canvas as the window.
canvas = Tk()
canvas.resizable(width=False,height=False)
canvas.geometry('300x130+500+200')
menu = MainMenu(canvas)
canvas.mainloop()
