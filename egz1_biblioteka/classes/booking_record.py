
import datetime

from classes.book import *
from classes.users import *

class BookingRecordType:
    ...


class Borrow(BookingRecordType):

    def __str__(self) -> str:
        return '-'


class Return(BookingRecordType):

    def __str__(self) -> str:
        return '+'


class BookingRecord:
    
    def __init__(self, id: int, type: BookingRecordType, user_id: str, book: Book) -> None:
        self.id = id # iraso id
        self.type = type
        self.user_id = user_id
        self.book = book
        self.created_on = datetime.datetime.now()
        self.returned_on = None

    def __str__(self) -> str:
        return f'{self.id} ({self.type}) "{self.user_id}" {self.book}'

    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other):
        if isinstance(other, BookingRecord):
            return (self.id == other.id)
        return False

    def __hash__(self):
        return hash(self.id)
