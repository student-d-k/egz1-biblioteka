
class Author:

    def __init__(self, author_name: str) -> None:
        self.author_name = author_name.capitalize()
        l = self.author_name.split()
        if len(l) > 0:
            self.author_short_name = f'{l[0][0]}. {l[1]}'
        else:
            self.author_short_name = author_name

    def __str__(self) -> str:
        return self.author_name

    def __repr__(self) -> str:
        return self.author_short_name
    
    def __eq__(self, other):
        if isinstance(other, Author):
            return (self.author_name == other.author_name)
        return False

    def __hash__(self):
        return hash(self.author_name)
