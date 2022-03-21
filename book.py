"""
    Description: This program defines a book class given title, author, year
    published, and file path name for book's text
    Author: Bhadra Rupesh
    Date: October 2021
"""

class Book(object):
    """ class for a single Book object """

    def __init__(self, title, author, year, filename):
        """ constructor for book object, given title, author, year published, and 
        filename/pathway """
        self.title = title
        self.author = author
        self.year = year
        self.filename = filename
        self.bookmark = 0

    def __str__(self):
        s = self.toString()
        return s

    def toString(self):
        return "%25s by %20s (%i)" % (self.title, self.author, self.year)

    def getTitle(self):
        return self.title

    def getAuthor(self):
        return self.author

    def getYear(self):
        return self.year

    def getFilename(self):
        return self.filename

    def getBookmark(self):
        return self.bookmark

    def setBookmark(self, newBookmark):
        self.bookmark = newBookmark
        return self.bookmark
       
    def getText(self):
        """ 
        Purpose: to get the whole text of the book in a single string, with lines
        separated by newline characters
        Parameters: self
        Return: content of book (str)
        """
        bookFile = open(self.filename, 'r')
        bookStr = ""
        for line in bookFile:
            if line[0] != "#":
                bookStr += (line)
        bookFile.close()
        return bookStr

    def getLinesList(self):
        """ 
        Purpose: to get the list (list) of lines (str) found in the book
        Parameters: self
        Return: lines list (list)
        """
        bookContents = self.getText()
        bookLinesList = bookContents.split("\n")
        return bookLinesList

    def getLinesPages(self, pageLength):
        """ 
        Purpose: to get the number of lines and number of pages in total of the book
        Parameters: self
        Return: number of lines, number of pages (list)
        """
        bookLinesList = self.getLinesList()
        numLines = len(bookLinesList)
        numPages = numLines // pageLength  # calculate total number of pages in book
        return numLines, numPages

if __name__ == '__main__':

    print("Testing the Book class...")
    myBook = Book("Gettysburg Address", "Abe Lincoln", 1863,
    "book-database/gettysburg.txt")

    print("Testing toString...")
    print(myBook)

    print("Testing getFilename...")
    print(myBook.getFilename())

    print("Testing getText...")
    text = myBook.getText()
    print(text[:105])                   # only print the first couple of lines

    print("bookmark is:", myBook.getBookmark())
    myBook.setBookmark(12)
    print("now bookmark is:", myBook.getBookmark())

    ################ Write additional tests below ###################

    print("Testing getAuthor...")
    author = myBook.getAuthor()
    print(author)

    print("Testing getYear...")
    year = myBook.getYear()
    print(year)

    
