
from abc import ABC, abstractmethod

class User:

    def __init__(self, id: str) -> None:
        self.id = id

    def __str__(self) -> str:
        return self.id

    def __repr__(self) -> str:
        return self.id
    
    def __eq__(self, other):
        if isinstance(other, User):
            return (self.id == other.id)
        return False

    def __hash__(self):
        return hash(self.id)


class Role:
    
    @abstractmethod
    def can_list_book(self) -> bool:
        pass

    @abstractmethod
    def can_add_book(self) -> bool:
        pass

    @abstractmethod
    def can_delete_book(self) -> bool:
        pass

    @abstractmethod
    def can_borrow_book(self) -> bool:
        pass


class Librarian(Role):

    def can_list_book(self) -> bool:
        return True

    def can_add_book(self) -> bool:
        return True

    def can_delete_book(self) -> bool:
        return True

    def can_borrow_book(self) -> bool:
        return True

    def __str__(self) -> str:
        return 'Bibliotekininkas'

    def __repr__(self) -> str:
        return 'B'


class Customer(Role):

    def can_list_book(self) -> bool:
        return True

    def can_add_book(self) -> bool:
        return False

    def can_delete_book(self) -> bool:
        return False

    def can_borrow_book(self) -> bool:
        return True

    def __str__(self) -> str:
        return 'Vartotojas'

    def __repr__(self) -> str:
        return 'V'
