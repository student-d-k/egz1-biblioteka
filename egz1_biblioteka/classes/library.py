
import os
import pickle

from classes.users import *
from classes.book import *
from classes.booking_record import *

BOOK_BORROW_MAX_DAYS = 7 # kiek laiko galima laikyti knyga

class Library:

    def __init__(self) -> None:
        self.users = {}
        self.books = {}
        # self.authors = {}
        self.booking_records = []
        self.genres = [Poetry(), Epic(), Fiction(), Story(), Children(), Detective()]


# 1 prideti knyga i biblioteka

def add_book_to_library(library: Library, role: Role, book: Book):
    """
    Adds books to library.

    Parameters:
    library (Library): The library where to add the book.
    role (Role): The role of the person attempting to add the book.
    book (Book): The book to be added.
    """

    try:

        if role.can_add_book():

            if book in library.books:
                library.books[book][0] += 1
            else:
                library.books[book] = 1

            print(f'Pridėjau knygą: "{book}".')

        else:
            print('Jūs neturite teisių pridėti knygos.')

    except Exception as e:

        print(e)

# 2 pasalinti senas knygas is bibliotekos

def delete_book_from_library(library: Library, role: Role, filter_function: callable):
    """
    Deletes books from the library based on a filter function.

    Parameters:
    library (Library): The library from which to delete books.
    role (Role): The role of the person attempting to delete the book.
    filter (callable): A function that takes a book and returns True if the book should be deleted.
    """

    try:

        if not role.can_delete_book():
            print('Jūs neturite teisių ištrinti knygos.')
            return

        delete_list_books = [e for e in filter(filter_function, library.books)]

        for book in delete_list_books:

            library.books.pop(book)
            print(f'Ištryniau knygą "{str(book)}"')

            delete_list_booking_records = [(i, br) for i, br in enumerate(library.booking_records) if br.book == book]
            delete_list_booking_records.sort(reverse=True, key=lambda x: x[0])

            for i, br in delete_list_booking_records:
                r = library.booking_records.pop(i)
                print(f'Ištryniau įrašą {str(r)}')

    except Exception as e:

        print(e)

# 3, 8 pasiimti knyga issinesimui

def borrow_book_from_library(library: Library, role: Role, user_id: User, book: Book):
    """
    Borrows book from the library based on a customer.

    Parameters:
    library (Library): The library from which to borrow book.
    role (Role): The role of the person attempting to borrow the book.
    user (User): The user attempting to borrow the book.
    book (Book): The book to be borrowed.
    """

    try:

        if not role.can_borrow_book(): 
            print('Jūs neturite teisių išsinuomoti knygos.')
            return

        if not book in library.books:
            print('Bibliotekoje nėra tokios knygos.')
            return

        if library.books[book] == 0:
            print('Visos knygos išnuomotos.')
            return

        delayed_books = [e.book for e in \
                        filter(lambda br: br.user_id == user_id and \
                                          (datetime.datetime.now()-br.created_on).days > BOOK_BORROW_MAX_DAYS, \
                        library.booking_records)]

        if len(delayed_books) > 0:
            print('Jūs turite laiku negrąžintų knygų.')
            return

        already_have_booking = [e.book for e in filter(lambda br: br.user_id == user_id and br.book == book, library.booking_records)]

        if len(already_have_booking) > 0:
            print('Jūs jau esate pasiėmęs šitą knygą.')
            return

        # pridedam irasa

        library.booking_records.append(BookingRecord(len(library.booking_records)+1, Borrow(), user_id, book))

        print(library.booking_records[-1])

    except Exception as e:

        print(e)

# 4, 5, 6, 7 ieskoti knygu pagal pavadinima arba autoriu arba pagal velavima

