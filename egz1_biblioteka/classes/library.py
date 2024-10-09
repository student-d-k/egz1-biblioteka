
import os
import pickle

import book

class Library:

    BOOKS_FILE_NAME = 'books.dat'
    BOOKS_FULL_FILE_NAME = '.\\data\\' + BOOKS_FILE_NAME

    def __init__(self) -> None:
        if os.path.isfile(self.BOOKS_FULL_FILE_NAME):
            dbfile = open(self.BOOKS_FULL_FILE_NAME, 'rb')    
            self.books = pickle.load(dbfile)
        else:
            self.books = ()

    def save(self) -> None:
        dbfile = open(self.BOOKS_FULL_FILE_NAME, 'wb')    
        pickle.dump(self.books)

if __name__ == "__main__":

    l = Library()
    l.books[Book('Salomėja Nėris', 'Eglė žalčių karalienė', 2019, 'Poezija')] = [1]
    l.save()

    print(Library().books)
