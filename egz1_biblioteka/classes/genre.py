
class Genre:
    ...


class Poetry(Genre):

    def __str__(self) -> str:
        return('Poezija')

    def __repr__(self) -> str:
        return('PO')


class Epic(Genre):

    def __str__(self) -> str:
        return('Epas')

    def __repr__(self) -> str:
        return('E')


class Fiction(Genre):

    def __str__(self) -> str:
        return('Grožinė literatūra')

    def __repr__(self) -> str:
        return('GL')


class Story(Genre):

    def __str__(self) -> str:
        return('Pasaka')

    def __repr__(self) -> str:
        return('PA')


class Children(Genre):

    def __str__(self) -> str:
        return('Vaikiška literatūra')

    def __repr__(self) -> str:
        return('V')


class Detective(Genre):

    def __str__(self) -> str:
        return('Detektyvas')

    def __repr__(self) -> str:
        return('D')
