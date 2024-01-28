#!/usr/bin/python

import sys
import random
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Canvas, ALL, NW

class Cons:
        
    BOARD_WIDTH = 300
    BOARD_HEIGHT = 300
    DELAY = 100
    DOT_SIZE = 10
    MAX_RAND_POS = 27


class Board(Canvas):

    def __init__(self):
        super().__init__(width=Cons.BOARD_WIDTH, height=Cons.BOARD_HEIGHT,
                         background="black", highlightthickness=0)
         
        self.init_game()
        self.pack()

    def init_game(self):
        """initializes game"""

        self.inGame = True
        self.dots = 3
        self.score = 0
        
        # variables used to move snake object
        self.moveX = Cons.DOT_SIZE
        self.moveY = 0
        
        # starting apple coordinates
        self.appleX = 100
        self.appleY = 190
        
        self.load_images()

        #self.focus_get()

        self.create_objects()
        self.locate_apple()
        self.bind_all("<Key>", self.on_key_pressed)
        self.after(Cons.DELAY, self.on_timer)

    def load_images(self):
        """loads images from the disk"""
        
        try:
            self.idot = Image.open("dot.png")
            self.dot = ImageTk.PhotoImage(self.idot)    
            self.ihead = Image.open("head.png")
            self.head = ImageTk.PhotoImage(self.ihead)           
            self.iapple = Image.open("apple.png")
            self.apple = ImageTk.PhotoImage(self.iapple) 

        except IOError as e:
            
            print(e)
            sys.exit(1)
        
    def create_objects(self):
        """creates objects on Canvas"""
    
        self.create_text(30, 10, text="Score: {0}".format(self.score), 
                         tag="score", fill="white")
        self.create_image(self.appleX, self.appleY, image=self.apple,
                          anchor=NW, tag="apple")
        self.create_image(50, 50, image=self.head, anchor=NW,  tag="head")
        self.create_image(30, 50, image=self.dot, anchor=NW, tag="dot")
        self.create_image(40, 50, image=self.dot, anchor=NW, tag="dot")
   
    def check_apple_collision(self):
        """checks if the head of snake collides with apple"""

        apple = self.find_withtag("apple")
        head = self.find_withtag("head")
        
        # print(self.bbox(head))
        
        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)
            
        for ovr in overlap:
          
            if apple[0] == ovr:
                
                self.score += 1
                x, y = self.coords(apple)
                self.create_image(x, y, image=self.dot, anchor=NW, tag="dot")
                self.locate_apple()

    def move_snake(self):
        """moves the Snake object"""
      
        dots = self.find_withtag("dot")
        head = self.find_withtag("head")
                
        items = dots + head
        
        z = 0
        while z < len(items)-1:
            
            c1 = self.coords(items[z])
            c2 = self.coords(items[z+1])
            self.move(items[z], c2[0]-c1[0], c2[1]-c1[1])
            z += 1
            
        self.move(head, self.moveX, self.moveY)     

    def check_collisions(self):
        """checks for collisions"""

        dots = self.find_withtag("dot")
        head = self.find_withtag("head")
        
        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)
        
        for dot in dots:
            for over in overlap:
                if over == dot:
                    self.inGame = False
            
        if x1 < 0:
            self.inGame = False
        
        if x1 > Cons.BOARD_WIDTH - Cons.DOT_SIZE:
            self.inGame = False

        if y1 < 0:
            self.inGame = False
        
        if y1 > Cons.BOARD_HEIGHT - Cons.DOT_SIZE:
            self.inGame = False

    def locate_apple(self):
        """places the apple object on Canvas"""
    
        apple = self.find_withtag("apple")
        self.delete(apple[0])
    
        r = random.randint(0, Cons.MAX_RAND_POS)
        self.appleX = r * Cons.DOT_SIZE
        r = random.randint(0, Cons.MAX_RAND_POS)
        self.appleY = r * Cons.DOT_SIZE
        
        self.create_image(self.appleX, self.appleY, anchor=NW,
            image=self.apple, tag="apple")

    def on_key_pressed(self, e): 
        """controls direction variables with cursor keys"""
    
        key = e.keysym

        LEFT_CURSOR_KEY = "Left"
        if key == LEFT_CURSOR_KEY and self.moveX <= 0:
            
            self.moveX = -Cons.DOT_SIZE
            self.moveY = 0
        
        RIGHT_CURSOR_KEY = "Right"
        if key == RIGHT_CURSOR_KEY and self.moveX >= 0:
            
            self.moveX = Cons.DOT_SIZE
            self.moveY = 0

        UP_CURSOR_KEY = "Up"
        if key == UP_CURSOR_KEY and self.moveY <= 0:
                        
            self.moveX = 0
            self.moveY = -Cons.DOT_SIZE

        DOWN_CURSOR_KEY = "Down"
        if key == DOWN_CURSOR_KEY and self.moveY >= 0:
            
            self.moveX = 0
            self.moveY = Cons.DOT_SIZE

    def on_timer(self):
        """creates a game cycle each timer event"""

        self.draw_score()
        self.check_collisions()

        if self.inGame:
            self.check_apple_collision()
            self.move_snake()
            self.after(Cons.DELAY, self.on_timer)
        else:
            self.game_over()            

    def draw_score(self):
        """draws score"""
        
        score = self.find_withtag("score")
        self.itemconfigure(score, text="Score: {0}".format(self.score))

    def game_over(self):
        """deletes all objects and draws game over message"""

        self.delete(ALL)
        self.create_text(self.winfo_width() /2, self.winfo_height()/2,
                         text="Game Over with score {0}".format(self.score), fill="white")


class Snake(Frame):

    def __init__(self):
        super().__init__()
                
        self.master.title('Snake')
        self.board = Board()
        self.pack()


def main():

    root = Tk()
    Snake()
    root.mainloop()  


if __name__ == '__main__':
    main()

