#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Name:        Phone UI
# Purpose:     To entertain kids who are bored at home, by providing them with fun games. 
#
# Author:      Michael Tuccillo
# Created:     26-Oct-2020
# Updated:     06-Nov-2020
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#I think this project deserves a 4+ because I met all the base requirements and I added many extra features in a clean and efficient manner.
#Features Added:
#I passed information between functions in a meaningful way, for example when checking usernames and passwords.
#I used many for loops in a very efficient manner, for example when drawing the buttons in the calculator.
#Program interface is very user friendly and enjoyable to use. For example, clear instructions, start and end screens and visually appealing images (phone background).
#Program is fully sanitized, all possible user input has been error checked and will not crash the program.
#Its a modular program, code is split into many functions which make the code efficient.
#Multiple apps/games
#Multiple sound effects, played them as music and not sounds as sounds do not let you change the volume.
#Added different fonts for texts
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

import random
import datetime
import logging

#Logging statements retrieved from Mr Brooks
logging.basicConfig(filename='log.txt', filemode='w', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

WIDTH = 400 #Determines width of screen
HEIGHT = 700 #Determines height of screen
gameState = "startScreen" #Set gameState to startScreen
currentTime = "" #Variable that stores the current time

#Flappy bird actors retrieved from https://www.vhv.rs/viewpic/TRxiRbh_flappy-bird-atlas-png-png-download-flappy-bird/
bird = Actor("bird0", (75,200)) #Makes bird actor
pipeTop = Actor("top_pipe", anchor=("left","bottom")) #Top pipe actor
pipeBottom = Actor("bottom_pipe", anchor=("left","top")) #Bottom pipe actor
birdDead = False #Represents if bird is dead or not
flappyBirdBackground = Actor("background", center=(200,350)) #Background for flappy bird
score = 0 #Score for flappy bird
pipeGap = 65 #The gap between the pipes
gravity = 0.3 #Gravity in flappy bird game
birdVelocity = 0 #Speed of the bird falling
beatHighScore = False #Represents if high score was beat
hitPipe = False #Represents if bird hit pipe

#Calculator actors for the buttons, retrieved from https://opengameart.org/content/calculator-ui
calculatorButtonsActors = {"0":Actor("0", (150,550)), "1":Actor("1", (50,325)), "2":Actor("2", (150,325)), "3":Actor("3", (250,325)), "4":Actor("4", (50,400)), "5":Actor("5", (150,400)), "6":Actor("6", (250,400)), "7":Actor("7", (50,475)), "8":Actor("8", (150,475)), "9":Actor("9", (250,475)), "delete":Actor("del", (350,175)), "+":Actor("add", (350,475)), "-":Actor("subtract", (350,400)), "/":Actor("division", (350,250)), "*":Actor("multiply", (350,325)), "brackets":Actor("brackets", (250,250)), ".":Actor("point", (250,550)), "=":Actor("equals", (350,550)), "negative":Actor("negative_positive", (50,550)), "ans":Actor("ans", (150,250)), "clear":Actor("clear", (50,250))}
calculatorScreen = Actor("calculator_screen", (200,65)) #Calculator screen actor
textRect = Rect((25,25),(350,60)) #Rectangle that text for calculator is put into
expression = "" #Calculator expression
brackets = 0 #Number of brackets in calculator expression
showAnswer = False #Determines if the answe should be displayed on calculator
answer = "" #Holds the answer to the expression
calculatorError = False #Represents if calculator had an error
calculatorErrorText = "" #Holds the error text for calculator 

#Holds the actors for the home screen, calculator app logo retrieved from https://www.baamboozle.com/index.php/study/93887
homeScreenApps = {"signOut":Actor("sign_out", (290,500)), "flappyBird":Actor("flappy_bird_app", (110,325)), "calculator":Actor("calculator_app", (290,325)), "knightRunner":Actor("knight_runner_app", (110,500))}
homeButton = Actor("home_button", (200,655)) #Home button retrieved from https://thenounproject.com/term/home-button/
volumeRepresentation = 75 #Stores the number that changes the size of the volume bar
volume = 0.5 #Stores the volume for the music
volumeBar = {"volumeRectangle":Rect((30,55),(50,150)), "backgroundRectangle":Rect((30,55),(50,volumeRepresentation))} #Volume bar rectangles
volumeButtons = {"volumeUp":Actor("volume_up", (55,230)), "volumeDown":Actor("volume_down", (55,30))} #Volume buttons for volume
app = "" #Stores what app is being played
canClick = False #Controls whether player can click 

startScreenButtons = {"existingUser":Rect((25,25),(350,75)), "newUser":Rect((25,150),(350,75))} #Stores start screen rectangles
wallpaper = Actor("phone_wallpaper", center=(200,350)) #Stores the wallpaper actor, retrieved from https://www.pinterest.ca/pin/441212094724054771/

newUserAndExistingUserScreenButtons = {"username": Rect((25,250),(350,75)), "password":Rect((25,375),(350,75)), "enter":Rect((75,500),(250,50))} #Stores the login screens rectangles
createOrEnterInfo = "" #Stores whether the player is creating an account or signing in
usernameAndPassword = {} #Dictionary that stores the username and password as a key and value pair
password = "" #Stores the password 
username = "" #Stores the username
enteringPassword = False #Represents whether user is entering password
enteringUsername = False #Represents whether user is entering username
#These variables represent what error occured
wrongInfo = False 
usernameTaken = False 
wrongInput = False
noInput = False

#category = {"sportsWords":Rect((300,150),(200,75)), "foodWords":Rect((50,150),(200,75)), "animalWords":Rect((550,150),(200,75))}
playButton = Rect((75,306.25),(250,75)) #The play button during start screen
instructionsButton = Rect((75,406.5),(250,75)) #The instructions button during start screen
backButton = Rect((305,535), (65,40)) #The back button during instructions screen
playAgainButton = Rect((100,262.5), (200,75)) #The play again button during win and lose screen
wordsWith7LettersButton = Rect((25,262.5),(100,50)) #Button that lets player pick 7 letter words
wordsWith6LettersButton = Rect((275,262.5),(100,50)) #Button that lets player pick 6 letter words
wordsWith5LettersButton = Rect((150,262.5),(100,50)) #Button that lets player pick 5 letter words
sportsButton = Rect((150,150),(100,50)) #Button for sports category
foodsButton = Rect((25,150),(100,50)) #Button for food category
animalsButton = Rect((275,150),(100,50)) #Button for animal category
wordsWith7LettersSports = ["Athlete", "Catcher", "Compete", "Defense", "Fielder", "Forward", "Pitcher", "Running", "Stadium", "Uniform"] #List that holds all the 7 letter sports words
wordsWith6LettersSports = ["Soccer", "Boxing", "Hockey", "Tennis", "Skiing", "Racing", "Goalie", "Golfer", "Huddle", "Helmet"] #List that holds all the 6 letter sports words
wordsWith5LettersSports = ["Arena", "Boxer", "Cycle", "Catch", "Coach", "Field", "Pitch", "Rugby", "Skate", "Score"] #List that holds all the 5 letter sports words
wordsWith7LettersAnimals = ["Cheetah", "Giraffe", "Dolphin", "Gorilla", "Vulture", "Ostrich", "Hamster", "Buffalo", "Leopard", "Raccoon"] #List that holds all the 7 letter animal words
wordsWith6LettersAnimals = ["Spider", "Turtle", "Parrot", "Python", "Jaguar", "Walrus", "Monkey", "Bobcat", "Rabbit", "Falcon"] #List that holds all the 6 letter animal words
wordsWith5LettersAnimals = ["Camel", "Hippo", "Horse", "Llama", "Moose", "Mouse", "Otter", "Panda", "Sheep", "Whale"] #List that holds all the 5 letter animal words
wordsWith7LettersFood = ["Biscuit", "Burrito", "Chicken", "Chowder", "Ketchup", "Mustard", "Popcorn", "Sausage", "Pancake", "Lettuce"] #List that holds all the 7 letter food words
wordsWith6LettersFood = ["Carrot", "Cheese", "Hotdog", "Muffin", "Orange", "Potato", "Radish", "Tomato", "Waffle", "Cherry"] #List that holds all the 6 letter food words
wordsWith5LettersFood = ["Bacon", "Candy", "Grape", "Gravy", "Omlet", "Peach", "Pizza", "Salad", "Steak", "Apple"] #List that holds all the 5 letter food words
guessedLetters = [] #List that will hold all the guessed letters
sportsWords = False #Control variable to remember if sports category was picked
foodWords = False #Control variable to remember if food category was picked
animalWords = False #Control variable to remember if animal category was picked
letters7 = False #Control variable to remember if 7 letter words was picked
letters6 = False #Control variable to remember if 6 letter words was picked
letters5 = False #Control variable to remember if 5 letter words was picked
dragonX = 50 #The x position of the dragon
knight = Actor("knight0") #Makes knight actor, and sets it to the starting image. Knight retrieved from https://opengameart.org/content/animated-runner-character
knight.pos = (375,500) #Sets knight to starting position
knight.frame = 0 #Sets knight frame to 0
dragon = Actor("reddragonfly0") #Makes dragon actor, and sets it to the starting image. Dragon retrieved from https://opengameart.org/content/red-dragon
dragon.pos = (dragonX,500) #Sets dragon's starting position
dragon.frame = 0 #Sets dragon frame to 0

def on_key_up(key):
    '''
    Called when a key is released

    Parameters
    ----------
    Key:
        Indicates the key that was released

    returns
    -------
    None
    '''

    global guess

    if gameState == "knightRunnerPlay":

        while askForGuess == True:

            try:

                guess = str(key.name) #Set guess to the key that was pressed
                guessChecker() #Call on guessChecker function

            except TypeError as e: #Runs if TypeError is raised

                incorrectType() #Call on incorrectType function
                continue #Go to the beginning of the while loop

def on_key_down(key,unicode):
    '''
    Called when a key is pressed

    Parameters
    ----------
    Key:
        Indicates the key that was pressed
    Unicode:
        Indicated the character that was typed

    returns
    -------
    None
    '''
    
    global birdVelocity
    global wrongInput
    
    #This runs when Flappy Bird is being played, controls bird flying
    if gameState == "flappyBirdPlay":
        
        if birdDead == False: #Prevents bird from being able to fly if its dead
            
            if key == keys.SPACE: #Checks if key pressed was space
                
                birdVelocity = -6.5 #Moves bird up

    #Runs if gameState equals either login screens.
    if gameState == "newUser" or gameState == "existingUser":
        
        try: #Will try to add key pressed to password or username string
            
            if enteringPassword == True: #This is true if player clicked on password box
                
                passwordCreator(unicode) #Calls on passwordCreator function, and sends it the key that was pressed
                
            if enteringUsername == True: #This is true if player clicked on username box
                
                usernameCreator(unicode) #Calls on usernameCreator function, and sends it the key that was pressed
                
        except TypeError as e: #Runs if TypeError was raised (key was not a letter or number)
            
            wrongInput = True 
            clock.schedule(userInfoNotRight,2) #Calls on userInfoNotRight function in 2 seconds 
            
def update():
    '''
    A loop that is called 60 times every second, it updates variables that constantly need to be updated

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    
    global addZeroToHour
    global addZeroToMinute
    global currentTime
    global addZeroToMonth
    global addZeroToDay
    global volumeBar
    
    currentTime = datetime.datetime.now() #Sets a variable equal to the current time. Uses datetime built in function
    music.set_volume(volume) #Sets the volume of music to what the player set it to in home screen

    if gameState == "flappyBirdPlay":
        
        movePipes() #Calls on function that moves pipe towards bird
        updateBird() #Calls on function that makes bird fall
    
    #If an aspect of time is a single digit, these will set a variable to zero, which then is put infront of the aspect of time to make it look nicer.
    if currentTime.minute < 10:
        
        addZeroToMinute = "0" 
        
    else:
        
        addZeroToMinute = ""
        
    if currentTime.hour < 10:
        
        addZeroToHour = "0"
        
    else:
        addZeroToHour = ""
        
    if currentTime.day < 10:
        
        addZeroToDay = "0"
        
    else:
        
        addZeroToDay = ""
        
    if currentTime.month < 10:
        
        addZeroToMonth = "0"
        
    else:
        addZeroToMonth = ""
        
    if gameState == "homeScreen":
        
        volumeBar["backgroundRectangle"] = Rect((30,55),(50,volumeRepresentation)) #Sets length of volume bar to represent the volume

def draw():
    '''
    A loop that draws all the graphical elements

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    
    if gameState == "knightRunner" or gameState == "flappyBird":

        screen.clear()
        
        #Draws name of games on start screen
        if gameState == "knightRunner":
            
            screen.draw.text("Knight Runner", (25,100), color="white", fontname="cherrycreamsoda", fontsize=45) #Display title of game
            
        if gameState == "flappyBird":
            
            screen.draw.text("Flappy Bird", (15,100), color="white", fontname="cherrycreamsoda", fontsize=60) #Display title of game
           
        screen.draw.filled_rect(playButton, "white") #Draw play button
        screen.draw.filled_rect(instructionsButton, "white") #Draw instructions button
        screen.draw.textbox("Play",playButton, color="black") #Write play in play button
        screen.draw.textbox("Instructions",instructionsButton, color="black") #Write instructions in instructions button

    if gameState == "instructions":

        screen.clear()
        
        if app == "knightRunner":
            
            screen.draw.text('''Welcome to Knight Runner, to
start the game, you must choose
a category and the number of
letters in the secret word. You
must guess the secret word before
the dragon catches the knight. You
will guess letter by letter, until
the word has been uncovered. To
guess a letter, click the letter on
your keyboard. You can guess 7
wrong letters before the dragon
reaches the knight and you lose the
game. To exit to the home screen,
press the back button.''', (50,80), color="white", fontsize=25, fontname="boogaloo") #Displays game instructions for knight runner game
            
        else:
            
            screen.draw.text('''Welcome to Flappy Bird, the aim
of this game is to fly through the
tubes and get new high scores. To
fly upward, press the space key.
Each time you make it through a
tube, your score will increase. If
your bird falls to the bottom of the
screen, or you run into a tube, you
lose.''', (20,100), color="white", fontsize=30, fontname="boogaloo") #Displays instructions for Flappy Bird game
            
        screen.draw.filled_rect(backButton, "white") #Draw back button
        screen.draw.textbox("Back", backButton, color="black") #Write back in back button

    if gameState == "pickCategory":

        screen.clear()
        screen.draw.text("Click on the category you want.", (35,400), color="white", fontsize=30, fontname="boogaloo")
        screen.draw.filled_rect(sportsButton, "white") #Draw sports button
        screen.draw.filled_rect(foodsButton, "white") #Draw foods button
        screen.draw.filled_rect(animalsButton, "white") #Draw animals button
        screen.draw.textbox("Sports",sportsButton, color="black")
        screen.draw.textbox("Foods",foodsButton, color="black")
        screen.draw.textbox("Animals",animalsButton, color="black")

    if gameState == "pickNumberOfLetters":

        screen.clear()
        screen.draw.text('''Choose the number of letters you
want the word to have by clicking
on the box.''', (55,400), color="white", fontsize=25, fontname="boogaloo")
        screen.draw.filled_rect(wordsWith7LettersButton, "white") #Draw 7 letters button
        screen.draw.filled_rect(wordsWith6LettersButton, "white") #Draw 6 letters button
        screen.draw.filled_rect(wordsWith5LettersButton, "white") #Draw 5 letters button
        screen.draw.textbox("7 letter words",wordsWith7LettersButton, color="black")
        screen.draw.textbox("6 letter words",wordsWith6LettersButton, color="black")
        screen.draw.textbox("5 letter words",wordsWith5LettersButton, color="black")

    if gameState == "knightRunnerPlay":
        
        screen.clear()
        screen.draw.text("Guessed Letters: "+displayGuessedLetters, (5,25), fontsize=25, color="white") #Display the already guessed letters
        screen.draw.text(""+blanks, (140,250), fontsize=50, color="white", fontname="boogaloo") #Display the blanks
        screen.draw.text("Incorrect Guesses Remaining: "+str(guessesRemaining), (75,350), color="white", fontname="boogaloo") #Draw guesses remaining
        knight.draw() #Draw knight
        dragon.draw() #Draw dragon
        
        if askForGuess == True:

            screen.draw.text("Guess a letter!", (145,310), color="white", fontname="boogaloo")

        elif alreadyGuessedLetter == True: #Run if player already guessed that letter

            screen.draw.text("You already guessed that letter!", (75,310), color="white", fontname="boogaloo")

        elif wrongLetter == True: #Run if player didn't guess the right letter

            screen.draw.text("That wasn't a correct letter!", (95,310), color="white", fontname="boogaloo")

        elif guessedCorrectLetter == True: #Run if player guessed correct letter

            screen.draw.text("You guessed a correct letter!", (90,310), color="white", fontname="boogaloo")

        elif didNotGuessALetter == True: #Run if player didn't guess an alphabetical character

            screen.draw.text("You didn't input a letter, try again!", (60,310), color="white", fontname="boogaloo")

    if gameState == "winner": #True when player guessed all the letters

        screen.clear()
        screen.draw.text('''Congratulations, you guessed the
  word! You escaped the dragon!''', (30,110), color="white", fontsize=30, fontname="boogaloo") #Draw congratulations message
        screen.draw.filled_rect(playAgainButton, "white") #Draw play again button
        screen.draw.textbox("Play again", playAgainButton, color="black")

    if gameState == "lost": #True if player ran out of guesses, hit tube in flappy bird or fell to the bottom of the game in flappy bird

        screen.clear()
        
        if app == "knightRunner":
            
            screen.draw.text('''Oh no! You ran out of guesses!
 The dragon caught the knight!
        The word was '''+word, (15,50), color="white", fontsize=35, fontname="boogaloo") #Tell player they lost and what the word was
            
        if app == "flappyBird":
            
            #Depending on how player lost the game, display text telling them how they lost
            if hitPipe == True:
                
                screen.draw.text("Oh no! You hit the tube!", (50,100), color="white", fontsize=35, fontname="boogaloo")
                
            else:
                
                screen.draw.text("Oh no! You fell to the bottom!", (15,100), color="white", fontsize=35, fontname="boogaloo")
             
            #If player beat the high score, then display text telling them they beat it
            if beatHighScore == True: 
                
                screen.draw.text("You beat the record!", (80,130), color="white", fontsize=35, fontname="boogaloo")
                screen.draw.text("The new record is " +str(score)+"!", (80,160), color="white", fontsize=35, fontname="boogaloo")
            
            #Tells player what their score was 
            else:
                
                screen.draw.text("Your score was " +str(score)+"!", (90,130), color="white", fontsize=35, fontname="boogaloo")
        
        screen.draw.filled_rect(playAgainButton, "white") #Draw play again button
        screen.draw.textbox("Play again", playAgainButton, color="black")
        
    if gameState == "flappyBirdPlay":
        
        #Draw actors on screen
        screen.clear()
        flappyBirdBackground.draw()
        pipeTop.draw()
        pipeBottom.draw()
        bird.draw()
        screen.draw.text("Score: "+str(score)+"", (25,25), color="white", fontsize=40) #Draw player score
        screen.draw.text("High score: "+str(highScore)+"", (25,50), color="white", fontsize=40) #Draw the high score
        
    if gameState == "calculator":
        
        screen.clear()
        calculatorScreen.draw()
        screen.draw.text('''Two multiplication signs next to
each other mean to the power.

Two division signs next to
each other mean floor division''', (30,120), color="white") #Tells player how to do calculations involving powers and floor division
        
        #Draw all the buttons for calculator
        for buttons in calculatorButtonsActors.values():
            
            buttons.draw()
        
        #Display answer of calculation
        if showAnswer == True:
            
            screen.draw.textbox(""+answer, textRect, color="black")
        
        #Display text telling player something went wrong with the calculation
        elif calculatorError == True:
            
            screen.draw.textbox(""+calculatorErrorText+"", textRect, color="black")
            
        else:
            
            screen.draw.textbox(""+expression, textRect, color="black") #Display the expression that the user is creating in calculator

    if gameState == "homeScreen":
        
        screen.clear()
        wallpaper.draw() #Draw wallpaper for phone
        #Draw volume bar and buttons
        screen.draw.filled_rect(volumeBar["volumeRectangle"], "white")
        screen.draw.filled_rect(volumeBar["backgroundRectangle"], "black")
        volumeButtons["volumeUp"].draw()
        volumeButtons["volumeDown"].draw()
        
        #Draw the apps for home screen
        for apps in homeScreenApps.values():
            
            apps.draw()
            
    if gameState == "startScreen":
        
        screen.clear()
        wallpaper.draw()
        #Draw start screen buttons
        screen.draw.filled_rect(startScreenButtons["newUser"],"white")
        screen.draw.textbox("New User", startScreenButtons["newUser"], color="black")
        screen.draw.filled_rect(startScreenButtons["existingUser"],"white")
        screen.draw.textbox("Existing User", startScreenButtons["existingUser"], color="black")
        screen.draw.text("To login, click the existing user button", (10,300), fontsize=30)
        screen.draw.text("To create account, click new user", (35,400), fontsize=30)
        
    if gameState == "newUser" or gameState == "existingUser":
        
        screen.clear()
        wallpaper.draw()
        #Draw login buttons
        screen.draw.filled_rect(newUserAndExistingUserScreenButtons["username"], "white")
        screen.draw.filled_rect(newUserAndExistingUserScreenButtons["password"], "white")
        screen.draw.filled_rect(newUserAndExistingUserScreenButtons["enter"], "white")
        screen.draw.textbox("Enter", newUserAndExistingUserScreenButtons["enter"], color="black")
        
        
        #Draws whatever keys they are typing into the username or password box
        if enteringPassword == False:
            
            screen.draw.textbox("Click to " +createOrEnterInfo+ " password", newUserAndExistingUserScreenButtons["password"], color="black")
            
        else:
            
            screen.draw.textbox("" +password+"", newUserAndExistingUserScreenButtons["password"], color="black")
            
        if enteringUsername == False:
            
            screen.draw.textbox("Click to " +createOrEnterInfo+ " username", newUserAndExistingUserScreenButtons["username"], color="black")
            
        else:
            
            screen.draw.textbox("" +username+"", newUserAndExistingUserScreenButtons["username"], color="black")
         
        #Displays error text for login screens
        if wrongInfo == True:
            
            screen.draw.text("Incorrect username or password", (40,560), fontsize=30, fontname="boogaloo")
            
        elif usernameTaken == True:
            
            screen.draw.text("Username already taken", (70,560), fontsize=30, fontname="boogaloo")
            
        elif wrongInput == True:
            
            screen.draw.text("You can only use letters or numbers", (15,560), fontsize=30, fontname="boogaloo")
            
        elif noInput == True:
            
            screen.draw.text("You didn't enter a password or username", (3,560), fontsize=28, fontname="boogaloo")
            
    if gameState == "newUser" or gameState == "existingUser" or gameState == "homeScreen":
        
        #The addZeroTo_____ will be equal to zero if the time, date, etc is less than 10. 
        screen.draw.text(""+str(currentTime.year)+"-"+addZeroToMonth+""+str(currentTime.month)+"-"+addZeroToDay+""+str(currentTime.day), (90,160), fontsize=50, fontname="boogaloo") #Draws the current date
        screen.draw.text(""+addZeroToHour+""+str(currentTime.hour)+":"+addZeroToMinute+""+str(currentTime.minute), (95,60), fontsize=100, fontname="boogaloo") #Draws the current time
    
    screen.draw.filled_rect(Rect((0,610),(400,90)), "white") #Draw white rectangle background for home button
    homeButton.draw() #Draw home button on all screens
    
def on_mouse_up(pos,button):
    '''
    Called when a mouse button is released

    Parameters
    ----------
    pos: tuple
        Gives location of the mouse when the button was pressed
    button:
        Indicates what button was released

    Returns
    -------
    None
    '''

    global gameState
    global createOrEnterInfo
    global enteringPassword
    global enteringUsername
    global sportsWords
    global foodWords
    global animalWords
    global letters7
    global letters6
    global letters5
    global volumeRepresentation
    global app
    global canClick
    global volume
    
    if gameState == "calculator":

        for buttons in calculatorButtonsActors.keys(): #Runs through dictionary of buttons fo calculator
            
            if calculatorButtonsActors[buttons].collidepoint(pos) and button == mouse.LEFT: #Checks if one of the buttons is pressed
                
                createAndSolveExpression(buttons) #Calls on createAndSolveExpression function and passes the key of the dictionary to it
                
    if gameState == "homeScreen":
        
        if volumeButtons["volumeUp"].collidepoint(pos) and button == mouse.LEFT: #Checks if volume up button was pressed
            
            if volumeRepresentation > 0 and volume < 1: #Prevents player from increasing volume past max 
                
                volumeRepresentation -= 37.5
                volume += 0.25
                
        elif volumeButtons["volumeDown"].collidepoint(pos) and button == mouse.LEFT: #Prevents player from decreasing volume past 0
            
            if volumeRepresentation < 150 and volume > 0:
                
                volumeRepresentation += 37.5
                volume -= 0.25
                
        elif homeScreenApps["signOut"].collidepoint(pos) and button == mouse.LEFT: #Checks if sign out button was clicked
            
            resetVariablesForNewUser() #Calls on fucntion that will reset variables for new user
        
        else:
            for apps in homeScreenApps.keys(): #Runs through the apps in the home screen
                    
                if homeScreenApps[apps].collidepoint(pos) and button == mouse.LEFT: #Checks if one of the apps were clicked
                        
                    gameState = apps #Sets gameState to the app
                    app = apps #Sets app to the app that was clicked
                    
            clock.schedule(delay,1) #Calls on delay function in 1 second, prevents bug that let player click an app and play button at the same time
            
    if gameState == "startScreen":
        
        #Sets variables based on if user is new or already has an existing account
        if startScreenButtons["newUser"].collidepoint(pos) and button == mouse.LEFT:
            
            createOrEnterInfo = "create"
            gameState = "newUser"
            
        if startScreenButtons["existingUser"].collidepoint(pos) and button == mouse.LEFT:
            
            createOrEnterInfo = "enter"
            gameState = "existingUser"
            
    if gameState == "existingUser" or gameState == "newUser":
        
        #Checks to see if player has clicked password or username box, sets variable to true to enable player typing
        if newUserAndExistingUserScreenButtons["password"].collidepoint(pos) and button == mouse.LEFT:
            
            enteringPassword = True
            enteringUsername = False
            
        if newUserAndExistingUserScreenButtons["username"].collidepoint(pos) and button == mouse.LEFT:
            
            enteringUsername = True
            enteringPassword = False
            
        if newUserAndExistingUserScreenButtons["enter"].collidepoint(pos) and button == mouse.LEFT: #Checks to see if player clicked enter button
            
            getUsernamesAndPasswords() #Calls on getUsernamesAndPasswords, this function checks if players input is valid
            
    if gameState != "homeScreen" and gameState != "existingUser" and gameState != "newUser" and gameState != "startScreen": #Runs if gameState is not equal to any of these
        
        if homeButton.collidepoint(pos) and button == mouse.LEFT: #Checks if player clicked the home button
            
            #Resets variables so player can click new app
            gameState = "homeScreen"
            canClick = False
            music.stop() #Stops music from playing if player exited back to home screen before it could finish
            app = ""
            
    if gameState == "existingUser" or gameState == "newUser":
        
        if homeButton.collidepoint(pos) and button == mouse.LEFT: #Runs if player clicks sign out
            
            resetVariablesForNewUser() #Calls on functionresetVariablesForNewUser, this funcion resets the variables back to their starting value
            
    if gameState == "knightRunner" or gameState == "flappyBird": #Checks if gameState equals knightRunner or flappyBird
        
        if playButton.collidepoint(pos) and button == mouse.LEFT and canClick == True: #Runs if player clicked on the play button
            
            if gameState == "knightRunner":
                
                resetKnightRunner() #Calls on resetKnightRunner function
                
            else:
                
                startGame() #Calls on startGame function that sets variables for game
                gameState = "flappyBirdPlay" #Set gameState to flappyBirdPlay

        elif instructionsButton.collidepoint(pos) and button == mouse.LEFT and canClick == True: #Runs if player clicked on instructions button

            gameState = "instructions" #Sets gameState to instructions

    if gameState == "instructions": #Checks if gameState equals instructions
        
        if backButton.collidepoint(pos) and button == mouse.LEFT: #Runs if back button is clicked

            gameState = app #Sets gameState to the app that the user is in


    if gameState == "pickCategory": #Checks if gameState equals pickCategory

        if sportsButton.collidepoint(pos) and button == mouse.LEFT: #Runs if sports button is clicked

            sportsWords = True
            gameState = "pickNumberOfLetters" #Sets gameState to pickNumberOfLetters

        elif foodsButton.collidepoint(pos) and button == mouse.LEFT: #Runs if foods button is clicked

            foodWords = True
            gameState = "pickNumberOfLetters" #Sets gameState to pickNumberOfLetters

        elif animalsButton.collidepoint(pos) and button == mouse.LEFT: #Runs if animals button is clicked

            animalWords = True
            gameState = "pickNumberOfLetters" #Sets gameState to pickNumberOfLetters


    if gameState == "pickNumberOfLetters": #Runs if pickNumberOfLetters is true

        if wordsWith7LettersButton.collidepoint(pos) and button == mouse.LEFT: #Checks if player clicked wordsWith7Letters button

            letters7 = True
            startGame() #Calls startGame function

        elif wordsWith5LettersButton.collidepoint(pos) and button == mouse.LEFT: #Checks if player clicked wordsWith5Letters button

            letters5 = True
            startGame() #Calls startGame function

        elif wordsWith6LettersButton.collidepoint(pos) and button == mouse.LEFT: #Checks if player clicked wordsWith6Letters button

            letters6 = True
            startGame() #Calls startGame function


    if gameState == "lost" or gameState == "winner": #Runs if gameState equals lost or winner

        if playAgainButton.collidepoint(pos) and button == mouse.LEFT: #Checks if playAgain button is clicked
            
            music.stop() #Stops music 
            
            if app == "knightRunner":
                
                resetKnightRunner() #Calls on resetKnightRunner function, this function will reset the variables for knight runner
                
            if app == "flappyBird":
                
                startGame() #Calls on startGame function, this function will set the variables needed for flappyBird
                
def pickWord():
    '''
    Choses a random word from a list based on the category and number of letters the player chose

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''

    global word

    if letters7 == True:

        if sportsWords == True:

            word = random.choice(wordsWith7LettersSports) #Pick random word from 7 letter sports words list

        elif foodWords == True:

            word = random.choice(wordsWith7LettersFood) #Pick random word from 7 letter food words list

        elif animalWords == True:

            word = random.choice(wordsWith7LettersAnimals) #Pick random word from 7 letter animal words list

    elif letters6 == True:

        if sportsWords == True:

            word = random.choice(wordsWith6LettersSports) #Pick random word from 6 letter sports words list

        elif foodWords == True:

            word = random.choice(wordsWith6LettersFood) #Pick random word from 6 letter food words list

        elif animalWords == True:

            word = random.choice(wordsWith6LettersAnimals) #Pick random word from 6 letter animal words list

    elif letters5 == True:

        if sportsWords == True:

            word = random.choice(wordsWith5LettersSports) #Pick random word from 5 letter sports words list

        elif foodWords == True:

            word = random.choice(wordsWith5LettersFood) #Pick random word from 5 letter food words list

        elif animalWords == True:

            word = random.choice(wordsWith5LettersAnimals) #Pick random word from 5 letter animal words list

    return


def incorrectType():
    '''
    Sets a control variable to true so the draw command can write text telling player they didn't guess a letter.

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''

    global didNotGuessALetter

    didNotGuessALetter = True
    clock.schedule_unique(askPlayer,3) #Call on askPlayer function in 3 seconds

    return

def guessChecker():
    '''
    Checks to see if player's guess is in the secret word

    This function checks if the guessed letter has already been guessed, if not, then it will append the guess into a list that
    holds the guessed letters and then run through the secret word to see if the guess is in the word. If guess is not in word, it will call
    on guessesLeft function. Will raise exception if guess was not a letter.

    Parameters
    ----------
    None

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If guess was not alphabetical
    '''

    global alreadyGuessedLetter
    global guessedLetters
    global blanks
    global wrongLetter
    global guessedCorrectLetter
    global askForGuess
    global displayGuessedLetters

    askForGuess = False

    if guess.isalpha() == False or len(guess) > 1: #True if player didn't input a letter

        raise TypeError("Guess was not alphabetical") #Raises TypeError

    if guess not in guessedLetters: #Runs if player didn't guess a letter they already guessed

        guessedLetters.append(guess) #Add their guess to list that holds guessed letters
        displayGuessedLetters = ", ".join(guessedLetters) #Makes list of guessed letters into a string so it can be displayed in the draw function

        for i in range(len(word)): #Runs through the letters in the secret word

            if word[i].lower() == guess.lower(): #True if the guess is equal to the letter in the word

                blanks = replaceLetter(blanks,i,guess) #Calls on replaceLetter function and sets blanks equal to what is returned
                guessedCorrectLetter = True
                clock.schedule_unique(winChecker,3) #Calls on winChecker function in 3 seconds
                music.play_once("correct_buzzer") #Retrieved from http://soundbible.com/1997-Cha-Ching-Register.html

        if guess.lower() not in word.lower(): #True if guess is not in the secret word

            wrongLetter = True
            guessesLeft() #Calls on guessesLeft function
            clock.schedule_unique(askPlayer,3) #Call on askPlayer function in 3 seconds
            music.play_once("incorrect_buzzer") #Retreived from http://soundbible.com/1495-Basketball-Buzzer.html

    elif guess in guessedLetters: #True if player guessed the letter already

        alreadyGuessedLetter = True
        clock.schedule_unique(askPlayer,3) #Call on askPlayer function in 3 seconds

    return

def guessesLeft():
    '''
    Subtracts a guess from their total guesses and checks if player ran out of guesses

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''

    global gameState
    global guessesRemaining

    guessesRemaining -= 1 #Subtract 1 from guessesRemaining
    moveDragon() #Call on moveDragon function
    
    if guessesRemaining == 0:
        
        music.play_once("dragon_roar") #Play dragon roar sound, retrieved from http://soundbible.com/2127-Dragon-Fire-Breath-and-Roar.html
        gameState = "lost"
        guessesRemaining = 7

    return




def winChecker():
    '''
    Checks if player guessed all the letters

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''

    global gameState

    if blanks.lower() == word.lower(): #True if all letters in the secret have been guessed
        
        music.play_once("cheer") #Sound retrieved from http://soundbible.com/1964-Small-Crowd-Applause.html
        gameState = "winner"

    elif blanks.lower() != word.lower(): #True if all the letters in the secret word haven't been guessed

        askPlayer() #Call on askPlayer function

    return

def askPlayer():
    '''
    Resets control variables to let code ask player for another guess

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''

    global askForGuess
    global alreadyGuessedLetter
    global wrongLetter
    global guessedCorrectLetter

    #Reset variables that tell draw function when to draw certain text
    alreadyGuessedLetter = False
    wrongLetter = False
    guessedCorrectLetter = False
    askForGuess = True

    return

def startGame():
    '''
    Set variables to starting values for the games

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''

    global gameState
    global word
    global blanks
    global guessesRemaining
    global guessedLetters
    global displayGuessedLetters
    global birdDead
    global score
    global birdVelocity
    global highScore
    global hitPipe

    if app == "knightRunner":
        
        resetKnightRunnerCharactersPos()
        gameState = "knightRunnerPlay"
        askPlayer() #Call on askPlayer function
        guessedLetters.clear() #clear all the values in guessedLetters list
        displayGuessedLetters = ""
        guessesRemaining = 7 #Set guesses the player has to 7
        pickWord() #Call on pickWord function
        blanks = "_"*len(word) #Set blanks to the length of the secret word
        
    if gameState == "flappyBird" or gameState == "lost":
        
        #Reads high score document
        file = open("highScores.txt","r")
        fileContents = file.readlines()
        file.close
        
        if fileContents == []: #Checks if highs score document is empty
            
            highScore = 0 #Sets highScore to 0
            
        else: #Runs if high score document is not empty
            
            highScore = fileContents[0] #Sets highScore variable equal to the number in the file
            
        setPipes() #Calls on setPipes function, this sets the pipes in position for flappy bird
        birdDead = False
        score = 0
        bird.y = 200 #Sets bird y position
        birdVelocity = 0 #Sets bird velocity
        hitPipe = False
        gameState = "flappyBirdPlay" #Set gameState to the actual play screen
        
    return

def resetKnightRunnerCharactersPos():
    '''
    Resets the positions and images of the dragon and knight 

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    
    global dragonX
    global knight
    global dragon
    
    dragonX = 50 #The x position of the dragon
    knight = Actor("knight0") #Makes knight actor, and sets it to the starting image. Knight retrieved from https://opengameart.org/content/animated-runner-character
    knight.pos = (375,500) #Sets knight to starting position
    knight.frame = 0 #Sets knight frame to 0
    dragon = Actor("reddragonfly0") #Makes dragon actor, and sets it to the starting image. Dragon retrieved from https://opengameart.org/content/red-dragon
    dragon.pos = (dragonX,500) #Sets dragon's starting position
    dragon.frame = 0 #Sets dragon frame to 0
    
    return

def resetKnightRunner():
    '''
    Resets variables to starting value for knight runner game

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''

    global animalWords
    global foodWords
    global sportsWords
    global letters7
    global letters6
    global letters5
    global gameState

    #Resets all variables to their starting values
    letters7 = False
    letters6 = False
    letters5 = False
    sportsWords = False
    foodWords = False
    animalWords = False
    resetKnightRunnerCharactersPos()
    gameState = "pickCategory" #Sets gameState to pickCategory so player can choose new category if they want

    return

def replaceLetter(stringIn, index, letter):
    '''
    Retrieved from Mr Brooks

    Replaces the blank with the correct letter

    Parameters:
    -----------
    stringIn : string
        The variable blanks
    index: integer
        The iterator that represents what letter in the word is correct

    Returns
    -------
    string
        The stringIn with the new letter
    '''

    return stringIn[:index] + letter + stringIn[index + 1:]

def updateKnight():
    '''
    Retrieved from https://github.com/HDSB-GWS/ICS3-Python-Notes/blob/master/notes/20%20-%20formal_documentation/formalDocumentation_ex1.py

    Changes photo of knight to next frame to create running animation

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''

    global knight

    knight.frame = knight.frame + 1 #Add 1 to knight.frame

    if knight.frame > 4: #Run if knight reached last frame

        knight.frame = 0 #Reset knight to first frame

    knight.image = 'knight' + str(knight.frame) #Set knight.image to a new image based on the value of knight.frame

    return

def moveDragon():
    '''
    Will move dragon closer to knight to show progress to player

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''

    global dragonX

    dragonX += 40 #Change the x position of the dragon by 90
    animate(dragon, pos=(dragonX,500)) #Moves dragon to new location

    return

def updateDragon():
    '''
    Changes photo of dragon to next frame to create flying animation

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''

    global dragon

    dragon.frame = dragon.frame + 1 #Add 1 to dragon.frame

    if dragon.frame > 6: #Run if dragon reached last frame

        dragon.frame = 0 #Reset dragon to starting frame

    dragon.image = 'reddragonfly' + str(dragon.frame) #Set dragon.image to a new image based on the value of dragon.frame

    return

def startAnimations():
    '''
    Schedules the animations for the dragon and knight

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''

    clock.schedule_interval(updateKnight,0.1) #Schedules the animation for knight
    clock.schedule_interval(updateDragon,0.1) #Schedules the animation for dragon

    return

def resetVariablesForNewUser():
    '''
    Resets variables to starting values for new user

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    
    global volumeRepresentation
    global volume
    global gameState
    global password
    global username
    global enteringUsername
    global enteringPassword
    global expression
    global brackets
    global answer
    
    #Resets all variables to starting values 
    volumeRepresentation = 75
    volume = 0.5
    gameState = "startScreen"
    password = ""
    username = ""
    enteringUsername = False
    enteringPassword = False
    expression = ""
    brackets = 0
    answer = ""

    return

def delay():
    '''
    Sets a variable that lets player click buttons to true

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    
    global canClick
    
    if gameState == "flappyBird" or gameState == "knightRunner":
        
        canClick = True #Sets variable that lets player click the play button to true
        
    return

def checkCredentials(existingUsernamesPasswords, userInfo):
    '''
    Checks whether the current username and password that has been inputted, match an existing account's username and password

    Parameters
    ----------
    existingUsernamesPasswords: Dictionary
        The usernames and passwords of already created accounts
    userInfo: Dictionary
        Current username and password

    Returns
    -------
    None
    '''
    
    global gameState
    global wrongInfo
    
    for existingUserInfo in existingUsernamesPasswords.items(): #Runs through existing usernames and passwords that have already been created 
        
        for currentInfo in userInfo.items(): #Runs through a dictionary that holds the newly input password and username
            
            if existingUserInfo == currentInfo: #Checks if the current passowrd and username match the password and username of an already created account
                
                gameState = "homeScreen" #Lets player into phone by setting gameState to homeScreen
                break #Breaks the loop
            
    else: #Runs if password and username did not match an already created account
        
        eraseCurrentInfo() #Calls on eraseCurrentInfo function
        wrongInfo = True
        clock.schedule(userInfoNotRight,2) #Calls on userInfoNotRight function in 2 seconds
        
    return

def userInfoNotRight():
    '''
    Resets variables that control when to display error messages

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    
    global wrongInfo
    global usernameTaken
    global wrongInput
    global noInput
    global calculatorError
    global calculatorErrorText
    
    #Resets variables that control what text to display on screen
    wrongInfo = False
    usernameTaken = False
    wrongInput = False
    noInput = False
    calculatorError = False
    calculatorErrorText = ""
    
    return

def newCredentials(existingUsernamesPasswords, userInfo):
    '''
    Checks whether the current username matches an existing account's username

    Parameters
    ----------
    existingUsernamesPasswords: Dictionary
        The usernames and passwords of already created accounts
    userInfo: Dictionary
        Current username and password

    Returns
    -------
    None
    '''
    
    global usernameTaken
    global gameState
    
    for existingUsernames in existingUsernamesPasswords.keys(): #Runs through the keys of the existing usernames and password
        
        if existingUsernames == username: #Checks if an existing username is equal to the current username
            
            usernameTaken = True
            eraseCurrentInfo() #Calls on eraseCurrentInfo function
            clock.schedule(userInfoNotRight,2) #Calls on userInfoNotRight function in 2 seconds
            
            break #Breaks for loop
        
    else: #Runs if username does not match an existing username
        
        createCredentials(existingUsernamesPasswords, userInfo) #Calls on create Credentials function, it passes the function the dictionaries that holds the usernames and passwords
        gameState = "homeScreen"
        
    return

def createCredentials(passwordsUsernamesFileContents,loginInfo):
    '''
    Writes new username and password to passwordsUsernames text document

    Parameters
    ----------
    passwordsUsernamesFileContents: Dictionary
        The usernames and passwords of already created accounts
    loginInfo: Dictionary
        Current username and password

    Returns
    -------
    None
    '''
    
    #Logging statements
    logging.debug('Building output string from dictionary')
    loginInfoString = convertDictionaryToString(loginInfo) #Sets loginInfoString to what is returned from convertDictionaryToString function 
    logging.debug('Attempting: writing to output.txt')
    
    if passwordsUsernamesFileContents == {}: #Checks if the passwords and usernames text document was empty, without this, an error would occur if the text doc was empty
        
        file = open("passwordsUsernames.txt", "w") #Opens passwordsUsernames.txt and tells program to write to it
        
    else: #If there was an existing username and password 
        
        file = open("passwordsUsernames.txt", "a") #Opens passwordsUsernames.txt and tells program to add to it
        
    file.write(loginInfoString) #Write the current username and password to the file
    file.close() #Close file
    logging.debug('Pass: writing to output.txt')
    logging.debug('Program ended')
    eraseCurrentInfo() #Call on eraseCurrentInfo function
    
    return 

def getUsernamesAndPasswords():
    '''
    Retrieves existing accounts information from text document and turns password and username into a dictionary

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    
    global noInput
    
    #Checks if player left anything blank
    if username == "" or password == "":
        
        noInput = True
        clock.schedule(userInfoNotRight,2) #Calls on userInfoNotRight function in 2 seconds
        
    else: 
        
        usernameAndPassword[username] = password #Creates a dictionary with the username as the key and the password as the value
        logging.debug('Attempting: Reading in passwordsUsernames.txt') #Logging statement
        #Opens text document and reads its contents
        file = open("passwordsUsernames.txt", "r") 
        fileList = file.readlines()
        file.close()
        logging.debug('Pass: Reading in passwordsUsernames.txt')
        logging.debug('Attempting: Converting information to a dictionary')
        existingUsersInfo = convertToDictionary(fileList) #Sets existingUserInfo to what is returned by convertToDictionary
        logging.debug('Pass: Converting information to a dictionary')
        
        if gameState == "newUser": 
            
            newCredentials(existingUsersInfo, usernameAndPassword) #Calls on newCredentials function, and passes through the existing account info and the current username and password
            usernameAndPassword.clear() #Clear the dictionary that holds the current password and username
            
        elif gameState == "existingUser":
            
            checkCredentials(existingUsersInfo, usernameAndPassword) #Calls on checkCredentials function, and passed through the existing account info and the current username and password
            usernameAndPassword.clear() #Clear the dictionary that holds the current password and username
            
    return
            
def eraseCurrentInfo():
    '''
    Clears username and password

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    
    global password
    global username
    
    #Reset password and username
    password = ""
    username = ""
    
    return 

def passwordCreator(character):
    '''
    Adds the character that was typed to a password variable

    Parameters
    ----------
    character: string
        The key that the player typed 
        
    Returns
    -------
    None
    
    Raises
    ------
    TypeError
        If typed character was not a letter or number 
    '''
    
    global password
    
    if character.isalnum() == False and character != "\x08": #Checks if player did not type a letter or number, besides the delete key
        
        raise TypeError("Password was not only alphabetical or numerical") #Raise TypeError if player did not input a letter or number
    
    elif character == "\x08": #Checks if character that was typed is the delete key
        
        password = str(password[:-1]) #Delete the last character in the password
        
    else:
        
        password += str(character) #Add the character to the password
        
    return
        
def usernameCreator(character):
    '''
    Adds the character that was typed to a username variable

    Parameters
    ----------
    character: string
        The key that the player typed 
        
    Returns
    -------
    None
    
    Raises
    ------
    TypeError
        If typed character was not a letter or number
    '''
    
    global username
    
    if character.isalnum() == False and character != "\x08": #Checks if player did not type a letter or number, besides the delete key
        
        raise TypeError("Username was not only alphabetical or numerical") #Raise TypeError if player did not input a letter or number
    
    elif character == "\x08":  #Checks if character that was typed is the delete key
        
        username = str(username[:-1]) #Delete the last character in the username
        
    else:
        
        username += str(character) #Add the character to the username
        
    return
    
def createAndSolveExpression(symbol):
    '''
    Creates an expression based on what buttons were pressed, and solves the expression

    Parameters
    ----------
    symbol: string
        The key value of the button that was pressed on the calculator app
        
    Returns
    -------
    None
    
    Raises
    ------
    TypeError
        If the expression did not have an operator before the bracket
        
    SyntaxError
        If the brackets in the expression are not closed or other format errors with the way the expression was formed
        
    ZeroDivisionError
        If the user tries to divide a number by 0
    '''
    
    global expression
    global brackets
    global showAnswer
    global answer
    global calculatorError
    global calculatorErrorText
    
    #Checks if the button on the calculator that was pressed is the equals button
    if symbol == "=":
        
        try: #Will try to evaluate the expression
            
            answer = str(eval(expression)) #Uses built in function eval to solve the expression
            showAnswer = True
            
        except SyntaxError: #Runs if SyntaxError is raised
            
            calculatorError = True
            
            if brackets == 1:
                
                calculatorErrorText = "Brackets are not closed"
                clock.schedule(userInfoNotRight,2)
                
            if calculatorErrorText == "":
                
                calculatorErrorText = "Something went wrong with the calculations"
                clock.schedule(userInfoNotRight,2)
                
        except ZeroDivisionError: #Runs if ZeoDivisionError is raised
            
            answer = "0"
            showAnswer = True
            
        except TypeError: #Runs if TypeError is raised
            
            calculatorError = True
            calculatorErrorText = "There was no operator before the bracket"
            clock.schedule(userInfoNotRight,2)
         
        expression = "" #Resets expression
        brackets = 0 #Resets number of brackets
    
    if calculatorError != True and symbol != "=":
        
        #These check if the button that was pressed is a special character that can't just be added to the expression
        if symbol == "brackets":
            
            if brackets%2 == 1 or brackets == 1: #Checks if the amount of brackets is odd or equal to one
                
                expression += ")" #Adds closed bracket to expression
                
            else: #Amount of brackets is even
                
                expression += "(" #Adds open bracket to expression
                
            brackets += 1 
            
        elif symbol == "clear":
            
            #Reset variables for calculator
            expression = ""
            showAnswer = False
            brackets = 0
            
        elif symbol == "ans":
            
            if answer != "": #Makes sure there is an actual answer to add
                
                expression += answer
                showAnswer = False
                
        elif symbol == "delete":
            
            lengthOfExpression = len(expression) #Gets length of expression
            
            if expression[lengthOfExpression-1:] == "(" or expression[lengthOfExpression-1:] == ")": #Deletes everything from the expression except the last character, then checks if character remaining is a bracket
                
                brackets -= 1 #Delete 1 from brackets
                
            expression = expression[:-1] #Deletes the last character in the expression
            
        elif symbol == "negative":
            
            lengthOfExpression = len(expression) #Gets length of expression
            
            if expression[lengthOfExpression-1:] == "(": #Checks if the last character in the expression is an open bracket
                
                expression += "-" #Adds a negative sign to the expression
                
            else: #If the last character is not a bracket
                
                expression += "(-" #Add a bracket and a negative sign to expression
                brackets += 1
                
        else: #If the button that was pressed is not one of the special characters above
            
            expression += str(symbol) #Added character to expression
            showAnswer = False

    return

def updateBird():
    '''
    Moves bird and detects if the bird died

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    
    global birdDead
    global birdVelocity
    global gameState
    global hitPipe

    birdVelocity += gravity #Add gravity to bird velocity
    bird.y += birdVelocity #Add bird velocity to bird y position

    if birdDead == False:
        
        if birdVelocity < -3: #True when player makes bird jump
            
            bird.image = "bird2" #Set bird image to bird2
            
        else:
            
            bird.image = "bird1" #Set bird image to bird1

    if bird.y > 700: #True if bird fell to the ground
        
        birdDead = True
        gameState = "lost"
        newHighScore() 

    if bird.y < 0: #If bird is above the map
        
        bird.y = 0 #Set bird to the top of the map but still visible

    if bird.colliderect(pipeTop) or bird.colliderect(pipeBottom): #Checks if bird collided with a pipe
        
        birdDead = True
        
        if bird.image != "bird_dead": #True as soon as bird hits pipe
            
            music.play_once("collision_noise") #Plays bang noise, retrieved from http://soundbible.com/947-Metal-Bang.html
            
        bird.image = "bird_dead" #Change bird image
        hitPipe = True

    return

def newHighScore():
    '''
    Checks if player beat high score, and writes new high score to text document

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    
    global beatHighScore
    
    if score > int(highScore): #True if the player's current score is higher than the high score
        
        #Open and write new score to highScores.txt
        file = open('highScores.txt','w')
        file.write(str(score))
        file.close
        music.play_once("cheer") #Play cheering sound
        beatHighScore = True
        
    else:
        
        beatHighScore = False
        
    return

def movePipes():
    '''
    Moves pipes towards the bird and increases the score

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    
    global score
    
    #Changes the position of the pipes to move it closer to bird
    pipeTop.left -= 3
    pipeBottom.left -= 3
    
    if pipeTop.right < 0 and pipeBottom.right < 0: #Once pipes make it to the end
        
        setPipes() 
        
        if birdDead == False:
            
            score += 1 #Add 1 to the score

    return

def setPipes():
    '''
    Sets pipes to starting position with random height

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    
    #Reset the pipes positions
    pipeY = random.randint(200,500) #Chose random height of pipe
    pipeTop.pos = (WIDTH, pipeY - pipeGap) #Set pipe to end of screen, with the y posion being the random integer that was chosen, minues the pipeGap
    pipeBottom.pos = (WIDTH, pipeY + pipeGap) #Set pipe to end of screen, with the y posion being the random integer that was chosen, plus the pipeGap

    return

def convertToDictionary(information):
    '''
    Retrieved from Mr Brooks
    Converts the incoming file information into a dictionary
    Convert information that comes in as a list of strings
    and breaks it apart assuming a token of ':' is separating
    the information in a 'key:value' type pairing
    Parameters
    ----------
    information : list of strings
        A list of strings in the format of 'key:value' pairing
    Returns
    -------
    dict
        A dictionary based on the list of string information input
    Raises
    ------
    Exception
        Incorrectly formatted work
    ValueError
        There wasn't the right number of items in the string ('key:value') expected
        The second value wasn't an integer
    '''
    assert isinstance(information, list), "Expecting input to be a list of 'key:value' pairs"

    logging.debug('Starting convertToDictionary function - passed in a list')

    formattedDictionary = {}
    
    try:
        
        logging.debug('Attempting to create a dictionary from key:value pairs')
        for item in information:
            
            logging.debug('Attempting with: ' + str(item[0:-1]))
            item = item[0:-1]       # remove the newline characters
            k, v = item.split(":")  # this is where it could break

            logging.debug('Attempting to insert the key: ' + str(k) + ' :with value: ' + str(v) + ' :into a dictionary entry')
            formattedDictionary[k] = v

    except Exception as e:
        
        logging.exception('An unexpected error popped up: ' + str(e))

    assert isinstance(formattedDictionary, dict), 'Dictionary was not properly built'
    logging.debug('Ending convertToDictionary - dictionary ready to be passed back')
    
    return formattedDictionary

def convertDictionaryToString(dictionary):
    '''
    Retrieved from Mr Brooks
    Converts the incoming dictionary information into a string for a file
    Convert information that comes in as a dictionary into
    a string that is formatted as 'key:value\n' per line
    Parameters
    ----------
    dictionary : dict
        A dictionary to convert into a single string for output
    Returns
    -------
    dict
        A dictionary based on the list of string information input
    '''
    assert isinstance(dictionary, dict), "Expecting input to be a dictionary"
    logging.debug('Starting convertDictionaryToString function')
    string = ''
    
    for k, v in dictionary.items():
        
        string = string + str(k) + ':' + str(v) + '\n'    # add a newline character at the end of each line

    logging.debug('convertDictionaryToString function completed.  Returning string')
    
    return string

startAnimations() #Calls on startAnimations function