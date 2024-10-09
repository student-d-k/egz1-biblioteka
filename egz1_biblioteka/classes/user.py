
class Bibliotekininkas:
    ...

class Vartotojas:
    ...

class User:
    def __init__(self, name: str, role: Bibliotekininkas | Vartotojas, password: str) -> None:
        self.name = name
        self.role = role
        self.password = password
    
