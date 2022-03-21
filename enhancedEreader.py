from enhancedSwindle import *
from os.path import isfile

def newUser(gw):
    """
        Purpose: Gets user's name if new user
        Parameters: None
        Return: owner's name (str)
    """
    width = gw.getWidth()
    height = gw.getHeight()

    lineCenter = Point(width/2, height/2 - 250)
    introText = Text(lineCenter, "\nSince this is the first time you used it,\n let's customize your Swindle...\n\nPlease enter your name: (Click anywhere to enter)")
    introText.setSize(25)
    introText.draw(gw)

    entryCenter = lineCenter.clone()
    entryCenter.move(0, 140)
    owner = Entry(entryCenter, 20)
    owner.setFill("white")
    owner.setSize(30)
    owner.draw(gw)
    gw.getMouse()
    ownerName = owner.getText()
    owner.undraw()

    welcomeCenter = entryCenter.clone()
    welcomeCenter.move(0, 100)
    welcomeText = Text(welcomeCenter, "Welcome to %s's Swindle v1.0!\n(Click anywhere to begin)" % ownerName)
    welcomeText.setSize(30)
    welcomeText.draw(gw)
    gw.getMouse()
    return ownerName

def oldUser(userSwindle):
    """
        Purpose: Starting screen for old user who logged back in
        Parameters: None
        Return: owner's name (str)
    """
    GW = userSwindle.gw
    width = GW.getWidth()
    height = GW.getHeight()
    
    welcomeCenter = Point(width/2, height/2 - 200)
    welcomeText = Text(welcomeCenter, "Welcome back to %s's Swindle v1.0!\n(Click anywhere to begin)" % userSwindle.getOwner())
    welcomeText.setSize(30)
    welcomeText.draw(GW)

    GW.getMouse()
    userSwindle.clearPage()
    return

def mainMenu(swindle):
    """
        Purpose: displays default main menu, with boxes for buttons
        Parameters: swindle
        Return: user's valid menu choice (int)
    """
    
    GW = swindle.gw
    width = GW.getWidth()
    height = GW.getHeight()

    buttonWidth = 500
    buttonHeight = 60

    option1Center = Point(width/2, height/4 + 20)
    option2Center = option1Center.clone()
    option2Center.move(0, buttonHeight + 20)
    option3Center = option2Center.clone()
    option3Center.move(0, buttonHeight + 20)
    option4Center = option3Center.clone()
    option4Center.move(0, buttonHeight + 20)

    option1Box = swindle.generateBox(option1Center, buttonWidth, buttonHeight)
    option1Box.draw(GW)
    option2Box = swindle.generateBox(option2Center, buttonWidth, buttonHeight)
    option2Box.draw(GW)
    option3Box = swindle.generateBox(option3Center, buttonWidth, buttonHeight)
    option3Box.draw(GW)
    option4Box = swindle.generateBox(option4Center, buttonWidth, buttonHeight)
    option4Box.draw(GW)

    option1Text = Text(option1Center, "1) Buy/See available books")
    option1Text.setSize(30)
    option1Text.draw(GW)

    option2Text = Text(option2Center, "2) See owned books")
    option2Text.setSize(30)
    option2Text.draw(GW)

    option3Text = Text(option3Center, "3) Read a book")
    option3Text.setSize(30)
    option3Text.draw(GW)

    option4Text = Text(option4Center, "4) Exit")
    option4Text.setSize(30)
    option4Text.draw(GW)

    while True:
        userClick = GW.getMouse()
        mouseX = userClick.x
        mouseY = userClick.y
        if (width/2 - buttonWidth/2) < mouseX < (width/2 + buttonWidth/2):
            if (option1Center.y - buttonHeight/2) < mouseY < (option1Center.y + buttonHeight/2):
                return 1
            elif (option2Center.y - buttonHeight/2) < mouseY < (option2Center.y + buttonHeight/2):
                return 2
            elif (option3Center.y - buttonHeight/2) < mouseY < (option3Center.y + buttonHeight/2):
                return 3
            elif (option4Center.y - buttonHeight/2) < mouseY < (option4Center.y + buttonHeight/2):
                return 4
            else:
                continue
        else:
            continue

def getData(ownedBooks, availableBooks):
    """
        Purpose: gets the string to write to the status.txt file with data
        Parameters: owned books list, availabe books list (lists of objects)
        Return: final string for status file
    """

    """
    file format:
    first line owner name
    space

    """
    ownedBookData = []
    availableBookData = []
    for ownedBook in ownedBooks:
        ownedBookData.append("owned:"+",".join([ownedBook.getTitle(), ownedBook.getAuthor(), str(ownedBook.getYear()), ownedBook.getFilename(), str(ownedBook.getBookmark())]))
    for availableBook in availableBooks:
        availableBookData.append("available:"+",".join([availableBook.getTitle(), availableBook.getAuthor(), str(availableBook.getYear()), availableBook.getFilename(), str(availableBook.getBookmark())]))
    joinedOwnedBookData = "\n".join(ownedBookData)
    joinedAvailableBookData = "\n".join(availableBookData)
    finalStr = joinedOwnedBookData + "\n" + joinedAvailableBookData
    return finalStr

def setData(filename):
    """
        Purpose: writes the data from the status file to the user who logged back in
        Parameters: file name with saved data
        Return: swindle object with updated data
    """
    statusFile = open(filename, "r")
    savedStatus = statusFile.read().split("\n")

    owner = savedStatus[0]
    userSwindle = Swindle(owner)

    ownedBookList = []
    availableBookList = []
    for book in savedStatus[2:]:
        bookLines = book.split(":")
        bookStatus = bookLines[0]
        bookData = bookLines[1].split(",")
        #index 0 is title, 1 is author, 2 is year, 3 is filename
        bookObject = Book(bookData[0], bookData[1], int(bookData[2]), bookData[3])
        #4 is bookmark page
        bookObject.setBookmark(int(bookData[4]))
        if bookStatus == "owned":
            ownedBookList.append(bookObject)
        elif bookStatus == "available":
            availableBookList.append(bookObject)
    userSwindle.setOwnedBooks(ownedBookList)
    userSwindle.setAvailableBooks(availableBookList)

    return userSwindle

if __name__ == '__main__':

    width = 700
    height = 900

    gw = GraphWin("Swindle", width, height)

    if isfile("status.txt"):
        userSwindle = setData("status.txt")
        userSwindle.setGw(gw)
        gw.setBackground("white")
        oldUser(userSwindle)
    else:
        owner = newUser(gw)                   # Display instructions and get user's name
        userSwindle = Swindle(owner)        # Create a new Swindle ereader for them
        userSwindle.setGw(gw)
        userSwindle.clearPage()
        gw.setBackground("white")

    while True:
        menuChoice = mainMenu(userSwindle)         # Display ereader's main menu
        if menuChoice == 1:
            userSwindle.buy()           # View available books with option to buy
        elif menuChoice == 2:
            userSwindle.showOwned()     # View owned books
        elif menuChoice == 3:
            userSwindle.read()          # Choose a book to read
        else:
            bookData = getData(userSwindle.getOwnedBooks(), userSwindle.getAvailableBooks())
            statusFile = open("status.txt", "w")
            statusFile.write("%s\n\n%s" % (userSwindle.getOwner(), bookData))
            statusFile.close()
            break                       # Turn off ereader (quit the program)

