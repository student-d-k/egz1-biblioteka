
import os
import pickle

from book import *

from pathlib import Path

class Library:

    BOOKS_FILE_NAME = 'books.dat'
    BOOKS_FOLDER_NAME = 'data'
    BOOKS_FULL_FILE_NAME = os.path.join(Path(__file__).resolve().parent.parent, BOOKS_FOLDER_NAME, BOOKS_FILE_NAME)

    def __init__(self) -> None:
        self.books = {}
        try:
            if os.path.isfile(self.BOOKS_FULL_FILE_NAME):
                with open(self.BOOKS_FULL_FILE_NAME, 'rb') as f:
                    self.books = pickle.load(f)
        except IOError as e:
            print("An error occurred:", e)
        except pickle.PickleError as e:
            print("An error occurred:", e)

    def save(self) -> None:
        try:
            with open(self.BOOKS_FULL_FILE_NAME, 'wb') as f:
                pickle.dump(self.books, f)
        except IOError as e:
            print("An error occurred:", e)

if __name__ == "__main__":

    l = Library()

    l.books[Book('Salomėja Nėris', 'Eglė žalčių karalienė', 2019, 'Poezija')] = [3]
    l.save()

    print(l.books)
