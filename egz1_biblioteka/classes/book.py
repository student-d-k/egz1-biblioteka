
from classes.author import *
from classes.genre import *

class Book:

    def __init__(self, author: Author, caption: str, year_of_release: int, genre: Genre) -> None:
        self.author = author
        self.caption = caption
        self.year_of_release = year_of_release
        self.genre = genre

    def __str__(self) -> str:
        return(f'{self.author}, {self.caption}, {self.genre} ({self.year_of_release})')

    def __repr__(self) -> str:
        return(f'{self.author.author_short_name}, {self.caption} ({self.year_of_release})')
    
    def __eq__(self, other):
        if isinstance(other, Book):
            return (self.author == other.author and
                    self.caption == other.caption and
                    self.year_of_release == other.year_of_release)
        return False

    def __hash__(self):
        return hash((self.author, self.caption, self.year_of_release))
