
import os
import pickle

from egz1_biblioteka.classes.users import *
from egz1_biblioteka.classes.book import *
from egz1_biblioteka.classes.booking_record import *

BOOK_BORROW_MAX_DAYS = 7 # kiek laiko galima laikyti knyga


class My1Library:

    def __init__(self) -> None:
        self.users = {}
        self.books = {}
        self.booking_records = []
        self.booking_records_history = []
        self.genres = [Poetry(), Epic(), Fiction(), Story(), Children(), Detective()]


# 1 prideti knyga i biblioteka

def add_book_to_library(library: My1Library, book: Book) -> str:
    'return error or empty string'

    try:

        if book in library.books:
            library.books[book][0] += 1
        else:
            library.books[book] = 1

        return ''

    except Exception as e:

        return str(e)


# 2 pasalinti knyga is bibliotekos

def delete_book_from_library(library: My1Library, book: Book) -> str:
    'return error or empty string'

    try:

        library.books.pop(book)

        delete_list_booking_records = [(i, br) for i, br in enumerate(library.booking_records) if br.book == book]
        delete_list_booking_records.sort(reverse=True, key=lambda x: x[0])

        # istrinam susijusius irasus ir booking_records

        for i, br in delete_list_booking_records:
            r = library.booking_records.pop(i)
            r.returned_on = datetime.datetime.now()
            library.booking_records_history.append(r)

        return ''

    except Exception as e:

        return str(e)


# help function

def book_count_in_library(library: My1Library, book: Book) -> int:
    'kiek knygos egzemplioriu liko bibliotekoje'

    booked_books = [e.book for e in filter(lambda br: br.book == book, library.booking_records)]
    return library.books[book][0] - len(booked_books)


# 3 pasiimti / grazinti knyga issinesimui

def borrow_book_from_library(library: My1Library, user_id: User, book: Book, action_return: bool) -> str:
    '''
    action_return = True - norim grazinti
    action_return = False - norim pasiskolinti
    return error or empty string
    '''

    try:

        if not book in library.books:
            return 'No such book in library'

        already_have_booking = [e.book for e in filter(lambda br: br.user_id == user_id and br.book == book, library.booking_records)]

        if action_return:

            if len(already_have_booking) == 0:
                return 'You have nothing to return'

            # istrinam irasa, perkeliam i istorija

            for i, br in enumerate(library.booking_records):
                if br.user_id == user_id and br.book == book:
                    r = library.booking_records.pop(i)
                    r.returned_on = datetime.datetime.now()
                    library.booking_records_history.append(r)
                    break

        else:

            if len(already_have_booking) > 0:
                return 'You have already booked this book'

            if book_count_in_library(library, book) < 1:
                return print('All books booked')

            # pridedam irasa

            library.booking_records.append(BookingRecord(len(library.booking_records)+1, Borrow(), user_id, book))

        return ''

    except Exception as e:
        return str(e)


# 4, 5, 6, 7 ieskoti knygu pagal pavadinima arba autoriu arba pagal velavima

def get_books_by_filter( 
    library: My1Library,
    search_str: str = '*',
    year_from: int = 1900,
    year_to: int = 2050,
    flag_overdued: bool = False,
    flag_available: bool = False,
    # flag_booked: bool = False) -> List[Book]:
    flag_booked: bool = False):

        if search_str == '*':
            filter_books_0 = [book for book in library.books if year_from <= book.year_of_release <= year_to]

        else:        
            filter_books_0 = [
                book for book in library.books
                if year_from <= book.year_of_release <= year_to
                and (search_str.lower() in book.author.author_name.lower() or search_str in book.caption.lower())
            ]

        if flag_overdued:
            overdued_books = [e.book for e in filter(lambda br: (datetime.datetime.now()-br.created_on).days > BOOK_BORROW_MAX_DAYS, library.booking_records)]

        if flag_available:
            available_books = [book for book in library.books if book_count_in_library(library, book) > 0]

        if flag_booked:
            booked_books = [e.book for e in library.booking_records]

        filter_books = [item for item in filter_books_0 if \
            (not flag_overdued or item in overdued_books) and \
            (not flag_available or item in available_books) and \
            (not flag_booked or item in booked_books)]

        return filter_books
