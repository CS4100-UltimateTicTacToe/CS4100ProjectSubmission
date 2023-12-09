import numpy as np
import tkinter as tk
from tkinter import *
import turtle as turtle

class Visual:
    def __init__(self, boardSize):
        self.boardSize = boardSize
        #Create the board
        self.board = [[0 for _ in range(self.boardSize)] for _ in range(self.boardSize)]
        #create the main window
        self.master = tk.Tk()
        #Create the canvas
        self.c_width = 500
        self.c_height= 500
        self.canvas = Canvas(self.master, width=self.c_width, height=(self.c_height+100))
        #create list order
        self.order = []

    def initialize_board(self):
        #Fill in the tic tac toe with spaces to make a move
        btn_x = 0
        btn_y = 0
        text_i = 0
        for i in range(0, self.boardSize):
            for k in range(0, self.boardSize):
                self.board[i][k] = Button(self.canvas, height=10, width=21, text='', bd=2, font=50)
                btn_x += 1
                text_i += 1
            btn_x = 0
            btn_y += 1

    #Mark the button with the symbol of the player that moved
    def add_to_order(self, turn, playerSymbol):
        self.order.insert(0, (self.board[turn[0]][turn[1]], playerSymbol, turn[0], turn[1]))

    def visualize_play(self):
        delay = 0
        for button in self.order:
            button[0].config(text=button[1])
            button[0].grid(row = button[2], column = button[3])
            # b = button  # capture current button in a new variable
            # self.master.after(delay, lambda b=b: b[0].config(text=b[1]))
            # self.master.after(delay, lambda b=b: b[0].grid(row = b[2], column = b[3]))
            delay += 1000

    #run the visualization
    def run_visual(self):
        #add button to board
        self.initialize_board()
        #visualize all the buttons
        self.visualize_play()
        #needed for the canvas to load
        self.canvas.pack()
        #Run the application
        self.master.mainloop()