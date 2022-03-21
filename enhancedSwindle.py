"""
    Description: This program defines a swindle class based on the owner's name
    after importing from the book class 
    Author: Bhadra Rupesh
    Date: October 2021
"""

from book import *
from graphics import *


def readBookDatabase(filename):
    """ read in book info from bookdb.txt, save each line as a Book object in list.
        This list will be returned and will serve as availableBooks. """
    infile = open(filename, 'r')
    availableBooks = []

    for book in infile:
        bookData = book.strip("\n").split(",")
        title = bookData[0]
        author = bookData[1]
        yearPublished = int(bookData[2])
        filePath = bookData[3]

        bookObject = Book(title, author, yearPublished, filePath)
        availableBooks.append(bookObject)

    return availableBooks

class Swindle(object):
    """ class for a single Swindle object """

    def __init__(self, owner):
        """ constructor for swindle object, given owner's name and graphics window"""
        self.owner = owner
        self.gw = ""
        self.ownedBooks = []
        self.availableBooks = readBookDatabase("bookdb-large.txt")    # list of Book objects
        self.pageLength = 20 # default initialization

    def __str__(self):
        """ pretty-print info about this object """
        s = "%s's Swindle:\nPage length set to %i lines" % (self.owner, self.pageLength)
        return s

    def getOwner(self):
        return self.owner

    def getGw(self):
        return self.gw

    def getOwnedBooks(self):
        return self.ownedBooks

    def getAvailableBooks(self):
        return self.availableBooks

    def getPageLength(self):
        return int(self.pageLength)

    def setOwner(self, newOwner):
        self.owner = newOwner
        return self.owner

    def setGw(self, newGw):
        self.gw = newGw
        return self.gw

    def setOwnedBooks(self, newOwned):
        self.ownedBooks = newOwned
        return self.ownedBooks

    def setAvailableBooks(self, newAvail):
        self.availableBooks = newAvail
        return self.availableBooks

    def setPageLength(self, newPageLength):
        self.pageLength = newPageLength
        return self.pageLength

    def getLetter(self, book, numPages):
        """ This method determines what the user wants to do next """
        GW = self.gw
        width = GW.getWidth()
        height = GW.getHeight()

        buttonWidth = 50
        buttonHeight = 50

        option1Center = Point(width/5 - buttonWidth/2, height/2 + 220)
        option2Center = option1Center.clone()
        option2Center.move(buttonWidth + height/5, 0)
        option3Center = option2Center.clone()
        option3Center.move(buttonWidth + height/5, 0)

        option1Box = self.generateBox(option1Center, buttonWidth, buttonHeight)
        option1Box.draw(GW)
        option2Box = self.generateBox(option2Center, buttonWidth, buttonHeight)
        option2Box.draw(GW)
        option3Box = self.generateBox(option3Center, buttonWidth, buttonHeight)
        option3Box.draw(GW)

        option1Text = Text(option1Center, "<")
        option1Text.setSize(30)
        option1Text.draw(GW)

        option2Text = Text(option2Center, "x")
        option2Text.setSize(30)
        option2Text.draw(GW)

        option3Text = Text(option3Center, ">")
        option3Text.setSize(30)
        option3Text.draw(GW)

        pageNumCenter = option2Center.clone()
        pageNumCenter.move(0, 100)

        while True:
            pageNumText = Text(pageNumCenter, "Page %i of %i" % (book.getBookmark() + 1, numPages))
            pageNumText.setSize(20)
            pageNumText.draw(GW)
            userClick = GW.getMouse()
            mouseX = userClick.x
            mouseY = userClick.y
            if (option1Center.y - buttonHeight/2) < mouseY < (option1Center.y + buttonHeight/2):
                if (option1Center.x - buttonWidth/2) < mouseX < (option1Center.x + buttonWidth/2):
                    if book.getBookmark() <= 0:
                        continue
                    else:
                        self.clearPage()
                        return 'p'
                elif (option2Center.x - buttonWidth/2) < mouseX < (option2Center.x + buttonWidth/2):
                    self.clearPage()
                    return 'q'
                elif (option3Center.x - buttonWidth/2) < mouseX < (option3Center.x + buttonWidth/2):
                    if book.getBookmark() >= numPages:
                        continue
                    else:
                        self.clearPage()
                        return 'n'
                else:
                    continue
            else:
                continue

    def clearPage(self):
        """ This method draw a white rectangle to clear the page """
        width = self.gw.getWidth()
        height = self.gw.getHeight()
        topMargin = 130
        lineSpacing = height/((self.pageLength)*1.85)
        textBottom = topMargin + lineSpacing*(self.pageLength)
        winClear = Rectangle(Point(0, topMargin), Point(width, textBottom + height/4))
        winClear.setFill("white")
        winClear.setOutline("white")
        winClear.draw(self.gw)
        return topMargin, lineSpacing, textBottom


    def displayPage(self, book):
        """ This method displays a single page at a time """
        width = self.gw.getWidth()
        height = self.gw.getHeight()
        topMargin, lineSpacing, textBottom = self.clearPage()
        numLines, numPages = book.getLinesPages(self.pageLength)
        bookLinesList = book.getLinesList()
        page = book.getBookmark()               # get current page (most recently read)
        pageStart = page * self.pageLength - 1
        # I edited the above line (- 1) because it wasn't showing the same result as in the sample
        pageEnd = pageStart + self.pageLength   # display 20 lines per page
        if pageEnd > numLines:
            pageEnd = numLines                  # in case you're at the end of the book
        for i in range(pageStart, pageEnd):
            lineCenter = Point(width/2, lineSpacing * ((i + 1) % 20) + topMargin + 10) 
            # the plus 10 is so that the center is not directly on the line of the margin
            textLine = Text(lineCenter, bookLinesList[i])
            textLine.draw(self.gw)
        if numPages == 1:                       # alter page numbers for 1-page books
            page = 1
        endPageLine = Text(Point(width/2, lineSpacing * numLines), "\nShowing page %d out of %d" % (page, numPages))
        endPageLine.draw(self.gw)
        return

    def displayText(self, book):
        """ This method allows the user to read one of their books.
            It calls displayPage() to show a single page at a time.
            It calls getLetter() to determine what the user wants to do next.
            When the user decides to quit reading a particular book, this method
            returns the (updated) Book object.
        """
        numLines, numPages = book.getLinesPages(self.pageLength)
        while True:
            self.displayPage(book)
            currentPage = book.getBookmark()
            choice = self.getLetter(book, numPages)       # user chooses to quit or read the next/previous page
            if choice == "q":               # quit reading and return to ereader
                return book
            elif choice == "n":                 # move on to the next page in the book
                bookContents = book.getText()   # unless user is on the last page
                currentLine = currentPage * self.pageLength
                if (currentLine + 1) < (numLines - self.pageLength):
                    book.setBookmark(currentPage+1)
                else:
                    continue
            else:                               # return to previous page in the book
                book.setBookmark(currentPage-1)
        return

    def generateBox(self, center, width, height):
        TL = center.clone()
        BR = center.clone()
        TL.move(-width/2, -height/2)
        BR.move(width/2, height/2)

        box = Rectangle(TL, BR)
        box.setFill("light gray")
        box.setOutline("light gray")
        return box

    def showOwned(self, prompt = "Click anywhere to exit."):
        """
        Purpose: Shows the books owned by the user
        Parameters: self, prompt (default click anywhere to exit)
        Return: prints owned books, returns owned books in list
        """
        GW = self.gw
        self.clearPage()

        if len(self.ownedBooks) == 0:
            prompt = "You don't own any books yet. Click anywhere to exit, and press button 1 to buy a book."

        textCenter = Point(GW.getWidth()/2, GW.getHeight()/2 - 350)
        text = Text(textCenter, prompt)
        text.draw(GW)

        for i in range(0, len(self.ownedBooks)):
            ownedBookStr = "%i: %s\n" % (i + 1, self.ownedBooks[i])
            ownedBookCenter = Point(GW.getWidth()/2 + 35, GW.getHeight()/2 - 100 + i*50)
            ownedBookText = Text(ownedBookCenter, ownedBookStr)
            ownedBookText.draw(GW)
            ownedBookText.setSize(20)
            boxCenter = ownedBookCenter.clone()
            boxCenter.move(-305, -10)
            bookBox = self.generateBox(boxCenter, 30, 30)
            bookBox.draw(GW)
        if prompt == "Click anywhere to exit." or len(self.ownedBooks) == 0:
            GW.getMouse()
            text.undraw()
            self.clearPage()
        return self.ownedBooks

    def showAvailable(self):
        """
        Purpose: Print the books available for user to buy
        Parameters: self
        Return: prints available books, returns available books in list
        """
        GW = self.gw
        for i in range(0, len(self.availableBooks)):
            availBookStr = "%i: %s\n" % (i + 1, self.availableBooks[i])
            availBookCenter = Point(GW.getWidth()/2 + 35, GW.getHeight()/2 - 100 + i*50)
            availBookText = Text(availBookCenter, availBookStr)
            availBookText.draw(GW)
            availBookText.setSize(20)
            boxCenter = availBookCenter.clone()
            boxCenter.move(-305, -10)
            bookBox = self.generateBox(boxCenter, 30, 30)
            bookBox.draw(GW)
        
        return self.availableBooks

    def getBookChoice(self, menuLength, prompt):
        """
        Purpose: Gets book choice from user based on prompt and menu length, needs typed input
        Parameters: self, length of menu to choose from (int), prompt to ask (str)
        Return: user's valid choice (int)
        """
        GW = self.gw
        width = GW.getWidth()
        height = GW.getHeight()
        #self.clearPage()
        promptTextCenter = Point(width/2, height/2 - 350)
        promptText = Text(promptTextCenter, prompt)
        promptText.draw(GW)
        entryCenter = Point(width/2, height/2)
        entryCenter.move(0, -height/4)
        while True:
            bookChoice = Entry(entryCenter, 20)
            bookChoice.setFill("white")
            bookChoice.setSize(30)
            bookChoice.draw(GW)
            GW.getMouse()
            choiceText = bookChoice.getText()
            try: 
                choiceInt = int(choiceText)
                if choiceInt <= menuLength:
                    bookChoice.undraw()
                    confirmText = Text(entryCenter, "You have chosen book %s." % choiceText)
                    confirmText.draw(GW)
                    confirmText.undraw()
                    promptText.undraw()
                    self.clearPage()
                    return choiceInt
                else:
                    bookChoice.undraw()
                    retryText = Text(entryCenter, "Invalid number. Please try again. Click to retry.")
                    retryText.draw(GW)
                    GW.getMouse()   
                    retryText.undraw()      
            except:
                bookChoice.undraw()
                retryText = Text(entryCenter, "Please enter an integer in the options. Click to retry.")
                retryText.draw(GW)
                GW.getMouse()
                retryText.undraw()

    def buy(self):
        """
        Purpose: Allows user to buy a book or skip
        Parameters: self
        Return: None, but buys book and moves it from available books to owned
        """
        self.clearPage()
        available = self.showAvailable()
        prompt = "\nWhich book would you like to buy? (0 to skip): "
        menuLength = len(available)
        if menuLength == 0:
            if menuLength == 0:
                noneLeft = ("There are no more books available for you to buy.")
                noneLeftText = Text(Point(self.gw.getWidth()/2, self.gw.getHeight()*0.75), noneLeft)
                noneLeftText.draw(self.gw)
                return
        else:
            while True:
                choice = self.getBookChoice(len(available), prompt)
                if choice != 0:
                    bookChoice = self.availableBooks[choice - 1]
                    self.ownedBooks.append(bookChoice)
                    self.availableBooks.pop(choice - 1)
                    #self.clearPage()
                    confirm = ("You've successfully purchased the book: %s" % bookChoice.getTitle())
                    confirmText = Text(Point(self.gw.getWidth()/2, self.gw.getHeight()*0.75), confirm)
                    confirmText.draw(self.gw)
                    return
                else:
                    return           

    def read(self):
        """
        Purpose: Allows user to read a book or skip
        Parameters: self
        Return: None, but leads to displaying book text if book chosen 
        """
        prompt = "\nWhich book would you like to read? (0 to skip): "
        menuLength = len(self.ownedBooks)
        if menuLength == 0:
            noneLeft = ("There are no books available for you to read. Please buy a book with button 1.")
            noneLeftText = Text(Point(self.gw.getWidth()/2, self.gw.getHeight()*0.75), noneLeft)
            noneLeftText.draw(self.gw)
            return
        else:
            owned = self.showOwned("")
            choice = self.getBookChoice(menuLength, prompt)
            if choice != 0:
                bookChoice = self.ownedBooks[choice - 1]
                self.displayText(bookChoice)
                self.clearPage()
                return
            else:
                return

    
            

if __name__ == '__main__':



    print("Testing the Swindle class...")
    owner = "Lionel"
    myswindle = Swindle(owner)
    print(myswindle)

    print("Testing showAvailable...")
    myswindle.showAvailable()

    print("Testing showOwned...")
    myswindle.showOwned()

    ################ Write additional tests below ###################

    print("Testing buy()...")
    myswindle.buy()

    print("Testing read()...")
    myswindle.read()