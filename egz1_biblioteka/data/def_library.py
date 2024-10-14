
from classes.library import *

def create_default_library() -> Library:

    new_library = Library()

    # add boooks

    new_library.books[Book(Author('Kazys Boruta'), 'Baltaragio malūnas', 1945, Epic())] = [2]
    new_library.books[Book(Author('Vincas Krėvė-Mickevičius'), 'Šiaudinėj pastogėj', 1935, Epic())] = [1]

    new_library.books[Book(Author('Antanas Baranauskas'), 'Anykščių šilelis', 1905, Fiction())] = [1]
    new_library.books[Book(Author('Antanas Baranauskas'), 'Anykščių šilelis', 2017, Fiction())] = [1]

    new_library.books[Book(Author('Salomėja Nėris'), 'Eglė žalčių karalienė', 1940, Story())] = [1]

    new_library.books[Book(Author('Eduardas Mieželaitis'), 'Zuikis Puikis', 1956, Children())] = [1]
    new_library.books[Book(Author('Vytautas V. Landsbergis'), 'Arklio Dominyko meilė', 1985, Children())] = [1]
    new_library.books[Book(Author('Antanas Vienuolis'), 'Paskenduolė', 1928, Children())] = [1]
    new_library.books[Book(Author('Jonas Biliūnas'), 'Laimės žiburys', 1905, Children())] = [1]

    new_library.books[Book(Author('Vytautas Petkevičius'), 'Molio Motiejus', 1978, Poetry())] = [1]
    new_library.books[Book(Author('Salomėja Nėris'), 'Eglė žalčių karalienė', 2019, Poetry())] = [1]
    new_library.books[Book(Author('Salomėja Nėris'), 'Poetry Collections', 1945, Poetry())] = [1]
    new_library.books[Book(Author('Eduardas Mieželaitis'), 'Mano Draugas', 1954, Poetry())] = [1]
    new_library.books[Book(Author('Justinas Marcinkevičius'), 'Mindaugas', 1968, Poetry())] = [1]
    new_library.books[Book(Author('Sigitas Geda'), 'Strazdas', 1972, Poetry())] = [1]
    new_library.books[Book(Author('Marcelijus Martinaitis'), 'Kukučio Baladės', 1977, Poetry())] = [1]
    new_library.books[Book(Author('Vytautas Mačernis'), 'Žmogaus Apnuoginta Širdis', 1980, Poetry())] = [1]
    new_library.books[Book(Author('Judita Vaičiūnaitė'), 'Pavasario Akvarelės', 1985, Poetry())] = [1]

    new_library.books[Book(Author('Vytautas Petkevičius'), 'Apie Viską ir Apie Nieko', 1972, Detective())] = [1]
    new_library.books[Book(Author('Rimantas Šavelis'), 'Šešėlių Žaidimas', 1978, Detective())] = [1]
    new_library.books[Book(Author('Algimantas Čekuolis'), 'Kryžkelės', 1980, Detective())] = [1]
    new_library.books[Book(Author('Vytautas Bubnys'), 'Alkana Žemė', 1982, Detective())] = [1]
    new_library.books[Book(Author('Rimantas Šavelis'), 'Mėnulio Šviesa', 1984, Detective())] = [1]
    new_library.books[Book(Author('Vytautas Petkevičius'), 'Dienos ir Naktys', 1986, Detective())] = [1]
    new_library.books[Book(Author('Algimantas Čekuolis'), 'Paskutinis Šūvis', 1989, Detective())] = [1]

    # add users

    new_library.users[User('Admin')] = [Librarian(), 'x']
    new_library.users[User('Marina')] = [Librarian(), 'x']

    new_library.users[User('01')] = [Customer(), 'x']
    new_library.users[User('02')] = [Customer(), 'x']
    new_library.users[User('03')] = [Customer(), 'x']
    new_library.users[User('04')] = [Customer(), 'x']
    new_library.users[User('05')] = [Customer(), 'x']

    # add boking records

    new_library.booking_records.append(BookingRecord(1, Borrow(), '01', Book(Author('Algimantas Čekuolis'), 'Kryžkelės', 1980, Detective())))
    new_library.booking_records[0].created_on = datetime.datetime.strptime("2024-10-01", "%Y-%m-%d")
    new_library.booking_records.append(BookingRecord(2, Borrow(), '02', Book(Author('Kazys Boruta'), 'Baltaragio malūnas', 1945, Epic())))
    new_library.booking_records[1].created_on = datetime.datetime.strptime("2024-10-05", "%Y-%m-%d")

    return new_library
