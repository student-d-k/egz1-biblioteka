
import os
import pickle

from classes.book import *
from classes.users import *
from classes.booking_record import *

from pathlib import Path

class Library:

    def __init__(self) -> None:
        self.users = {}
        self.books = {}
        self.authors = {}
        self.booking_records = []
