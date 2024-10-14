
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
        self.booking_records = []
        self.genres = [Poetry(), Epic(), Fiction(), Story(), Children(), Detective()]


# 1 prideti knyga i biblioteka

def add_book_to_library(library: Library, book: Book) -> str:
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

def delete_book_from_library(library: Library, book: Book) -> str:
    'return error or empty string'

    try:

        library.books.pop(book)

        delete_list_booking_records = [(i, br) for i, br in enumerate(library.booking_records) if br.book == book]
        delete_list_booking_records.sort(reverse=True, key=lambda x: x[0])

        # istrinam susijusius irasus ir booking_records

        for i, br in delete_list_booking_records:
            r = library.booking_records.pop(i)

        return ''

    except Exception as e:

        return str(e)


# help function

def available_books(library: Library, book: Book) -> int:
    'kiek knygos egzemplioriu liko bibliotekoje'

    booked_books = [e.book for e in filter(lambda br: br.book == book, library.booking_records)]
    return library.books[book] - len(booked_books)


# 3 pasiimti knyga issinesimui

def borrow_book_from_library(library: Library, user_id: User, book: Book):
    'return error or empty string'

    try:

        if not book in library.books:
            return 'No such book in library'

        already_have_booking = [e.book for e in filter(lambda br: br.user_id == user_id and br.book == book, library.booking_records)]

        if len(already_have_booking) > 0:
            return 'You have already booked this book'

        if available_books(library, book) < 1:
            return print('All books booked')

        # pridedam irasa

        library.booking_records.append(BookingRecord(len(library.booking_records)+1, Borrow(), user_id, book))

        return ''

    except Exception as e:
        return str(e)


# 4, 5, 6, 7 ieskoti knygu pagal pavadinima arba autoriu arba pagal velavima

def get_books_by_filter(library: Library, search_str: str, year_from: int, year_to: int, only_overdued: bool, only_available: bool) -> [Book]:

        if search_str == '*':
            filter_books_0 = [book for book in library.books if year_from <= book.year_of_release <= year_to]

        else:        
            filter_books_0 = [
                book for book in library.books
                if year_from <= book.year_of_release <= year_to
                and (search_str.lower() in book.author.author_name.lower() or search_str in book.caption.lower())
            ]

        if only_overdued:
            overdued_books = [e.book for e in filter(lambda br: (datetime.datetime.now()-br.created_on).days > BOOK_BORROW_MAX_DAYS, library.booking_records)]

        if only_available:
            available_books = [book for book in library.books if available_books(library, book) > 0]

        if only_overdued:
            if only_available:
                filter_books = [item for item in filter_books_0 if item in overdued_books and item in available_books]
            else:
                filter_books = [item for item in filter_books_0 if item in overdued_books]
        else:
            if only_available:
                filter_books = [item for item in filter_books_0 if item in available_books]
            else:
                filter_books = filter_books_0

        return filter_books
