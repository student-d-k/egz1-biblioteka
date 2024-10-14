
import os
import pickle

from classes.book import *
from classes.users import *
from classes.booking_record import *

BOOK_BORROW_MAX_DAYS = 7 # kiek laiko galima laikyti knyga

class Library:

    def __init__(self) -> None:
        self.users = {}
        self.books = {}
        self.authors = {}
        self.booking_records = []
        self.genres = [Poetry(), Epic(), Fiction(), Story(), Children(), Detective()]
