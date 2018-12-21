"""
Program: Battleships Unicorn Hat display
Author: Tim Mulford
Date: 08/02/2015
Version: 0.2
Python3
"""

#import libraries
import unicornhat as unicorn
import time, random

# create initial grid
def create_sea():
    # initialise blank grid
    grid = [[0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0]]

    # generate position for battleship
    x = random.randint(0,3)
    y = random.randint(0,7)

    # place battleship
    for a in range(5):
        grid[y][x+a]=1

    # generate co-ordinate for cruiser
    x = random.randint(0,5)
    y = random.randint(0,7)

    # check if the generated co-ordinates are clear
    # regenerate co-ordinates until a clear position is found
    while [grid[y][x],grid[y][x+1],grid[y][x+2]] != [0,0,0]:
        x = random.randint(0,5)
        y = random.randint(0,7)

    # place cruiser
    for a in range(3):
        grid[y][x+a]=1

    # generate co-ordintes for patrol boat   
    x = random.randint(0,6)
    y = random.randint(0,7)

    # check if the geneated co-ordinates are clear
    # regenerate co-ordinates until a clear position is found
    while [grid[y][x],grid[y][x+1]] != [0,0]:
        x = random.randint(0,6)
        y = random.randint(0,7)

    # place patrol boat
    for a in range(2):
        grid[y][x+a]=1

    # used for testing grid generated properly
    # displays grid to screen
    #for row in grid:
    #    print(row)
        
    return(grid)

# display the current state of the sea
# blue LED for undisturbed sea
# red LED for HIT
# unlit for MISS
def display_sea(sea):
    for y in range(8):
        for x in range(8):
            if sea[y][x] == 0 or sea[y][x] == 1:
                unicorn.set_pixel(x,y,79,106,226)
            if sea[y][x] == 2:
                unicorn.set_pixel(x,y,66,68,77)
            if sea[y][x] == 3:
                unicorn.set_pixel(x,y,214,28,31)
    unicorn.show()

# set the whole display to colour of the passed RGB code
def flood_colour(red,green,blue):
    for x in range(8):
        for y in range(8):
            unicorn.set_pixel(x,y,red,green,blue)
    unicorn.show()

# repeat game loop
while True:

    # initilse game conditions
    sea = create_sea()
    ammo = 20
    ships = 10
    game_over = False

    # display game grid on unicorn hat
    display_sea(sea)

    # repeat until end of game condition met
    while game_over == False:

        # display remaining ammo
        print("You have",ammo,"shots left")
        
        # capture x co-ordinate from player
        x = int(input("Enter the x co-ordinate for your shot: ")) - 1

        while x not in (0,1,2,3,4,5,6,7):
            print(x+1,"is not in range try again")
            x = int(input("Enter the x co-ordinate for your shot: ")) - 1
            
        for a in range(8):
            unicorn.set_pixel(x,a,0,150,0)
            unicorn.show()
            time.sleep(0.05)
                

        # capture y co-ordinate from player
        y = 8 - int(input("Enter the y co-ordinate for your shot: "))

        while y not in (0,1,2,3,4,5,6,7):
            print(8 - y,"is not in range try again")
            y = 8 - int(input("Enter the y co-ordinate for your shot: "))

        for a in range(8):
            unicorn.set_pixel(a,y,0,150,0)
            unicorn.show()
            time.sleep(0.05)

        # pause 1 second
        time.sleep(1)

        # highlight aimed co-ordinate
        
        for a in range(0,255,5):
            unicorn.set_pixel(x,y,a,a,a)
            unicorn.show()
            
        for a in range(0,255,5):
            unicorn.set_pixel(x,y,255-a,255-a,255-a)
            unicorn.show()

        # check if shot is a hit
        # if a ship is hit flash green to unicorn hat and update number
        # of remaining ships and grid.
        # if the shot misses flash red to unicorn hat.
        # Update grid and display updated sea on the unicorn hat
        if sea[y][x] == 1:
            print("Hit")
            for repeat in range(3):
                flood_colour(0,255,0)
                time.sleep(0.2)
                flood_colour(0,0,0)
                time.sleep(0.2)
                
            sea[y][x] = 3
            ships = ships - 1
            display_sea(sea)
            
        else:
            print("Miss")
            for repeat in range(3):
                flood_colour(255,0,0)
                time.sleep(0.2)
                flood_colour(0,0,0)
                time.sleep(0.2)
                
            sea[y][x] = 2
            ammo = ammo - 1
            display_sea(sea)

        # check if either game over condition has been met.
        # if it has set game_over to true
        if ships == 0 or ammo == 0:
            game_over = True

    # if game was ended with no ammo
    # display defeat animation on unicorn hat
    if ammo == 0:
        print("Our fleet is defeated.")
        for y in range(8):
            for x in range(8):
                for fade in range(0,255,50):
                    unicorn.set_pixel(x,y,255,255-fade,255-fade)
                    unicorn.show()
            
    # if game was ended with no ships left
    # display victory animation on unicorn hat
    if ships == 0:
        print("Our fleet is victorious.")
        for y in range(8):
            for x in range(8):
                for fade in range(0,255,50):
                    unicorn.set_pixel(x,y,255-fade,255,255-fade)
                    unicorn.show()

    # prompt user for a rematch
    # if the user says no then break loop and end program
    repeat = input("Do you want a rematch? ").lower()

    if repeat in ["no","n"]:
        print("Thanks for playing")
        break
    
