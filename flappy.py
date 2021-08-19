
#
# Flappy Canvas.py
#

# How to Play
print(
"""HOW TO PLAY\n
The \"Player\" (The Circle) will follow your mouse at all times.\n
Waves of increasingly quicker & larger mines come your way, you must avoid these mines at all costs. \n
Every 4 difficulty (or score) increase will increase your amount of boosts by 1. When you have a boost, you may left click to activate invulnerability for a short moment.\n
Good Luck!
""")

# Imports
from random import randint
from math import floor
from cmu_graphics import *

# Defining Variables
app.stepsPerSecond = 7
app.background = gradient('white', 'white', 'gray', start='left')
difficulty = 1
cursor = Circle(100, 200, 10, border='black', borderWidth=5, fill='white')
mines = Group();
boosts = 1
boostLabel = Label("You have " + str(floor(boosts)) + " boosts", 50 ,15)
scoreLabel = Label("Your Score is " + str(difficulty), 50 ,30)
counter = 0
boostActive = counter

# Function to generate mines
def generateMines(counter):
    global difficulty
    size=difficulty/2

    # Size limit to keep game possible
    if(size>=15):
        size=15

    # Mine Generator
    for x in range(4):
        mines.add(Circle(400, randint(-10, 400), size+2, fill='red'))

    # Difficulty Multiplyer
    if(counter >= difficulty*40):
        difficulty+=1
        scoreLabel.value = "Your Score is " + str(difficulty)

        global boosts
        boosts+=0.25
        app.stepsPerSecond*=1.05
        print(f"\n\nDifficulty has been increased. \nSize={size+2} \nNew Mine Frequency={pythonRound(10/app.stepsPerSecond, 2)}/s")

# Update mouse cursor on mouse move
def onMouseMove(mouseX, mouseY):
    cursor.centerX=mouseX
    cursor.centerY=mouseY

    # Randomize cursor border colour when boosting
    if(boostActive):
        cursor.border=rgb(randint(0, 255), randint(0, 255), randint(0, 255))

# Boost Activation
def onMousePress(mouseX, mouseY):
    global boosts
    global boostActive
    if(boosts >= 1 and boostActive == False):
        boostActive=counter
        boosts-=1

# Function called every x seconds depending on difficulty
def onStep():

    # Move All Mines by 5
    mines.centerX-=5

    # Update Tracker Of Total Steps
    global counter
    counter+=1

    # Boost Expiry
    global boostActive
    if(counter >= boostActive+70):
        boostActive=False
        boostLabel.value="You have " + str(floor(boosts)) + " boosts"
        cursor.border='black'

    # Summons mines every 10 steps
    if(counter % 10 == 5):
        generateMines(counter)

    # Loss Detection
    if(mines.hitsShape(cursor) and boostActive == False):
        mines.clear()
        Label("You Lost!", 200, 200, size=50, bold=True)
        Label(f"You reached a score of {difficulty}!", 200, 250, size=25, bold=True)
        app.stop()
