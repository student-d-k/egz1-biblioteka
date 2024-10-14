
from classes.library import *

def create_default_library() -> Library:

    new_library = Library()

    # add boooks

    new_library.books[Book(Author('Kazys Boruta'), 'Baltaragio malūnas', 1945, Epic())] = [4]
    new_library.books[Book(Author('Vincas Krėvė-Mickevičius'), 'Šiaudinėj pastogėj', 1935, Epic())] = [3]

    new_library.books[Book(Author('Antanas Baranauskas'), 'Anykščių šilelis', 1905, Fiction())] = [1]
    new_library.books[Book(Author('Antanas Baranauskas'), 'Anykščių šilelis', 2017, Fiction())] = [5]

    new_library.books[Book(Author('Salomėja Nėris'), 'Eglė žalčių karalienė', 1940, Story())] = [8]

    new_library.books[Book(Author('Eduardas Mieželaitis'), 'Zuikis Puikis', 1956, Children())] = [2]
    new_library.books[Book(Author('Vytautas V. Landsbergis'), 'Arklio Dominyko meilė', 1985, Children())] = [1]
    new_library.books[Book(Author('Antanas Vienuolis'), 'Paskenduolė', 1928, Children())] = [5]
    new_library.books[Book(Author('Jonas Biliūnas'), 'Laimės žiburys', 1905, Children())] = [6]

    new_library.books[Book(Author('Vytautas Petkevičius'), 'Molio Motiejus', 1978, Poetry())] = [1]
    new_library.books[Book(Author('Salomėja Nėris'), 'Eglė žalčių karalienė', 2019, Poetry())] = [3]
    new_library.books[Book(Author('Salomėja Nėris'), 'Poetry Collections', 1945, Poetry())] = [8]
    new_library.books[Book(Author('Eduardas Mieželaitis'), 'Mano Draugas', 1954, Poetry())] = [7]
    new_library.books[Book(Author('Justinas Marcinkevičius'), 'Mindaugas', 1968, Poetry())] = [9]
    new_library.books[Book(Author('Sigitas Geda'), 'Strazdas', 1972, Poetry())] = [8]
    new_library.books[Book(Author('Marcelijus Martinaitis'), 'Kukučio Baladės', 1977, Poetry())] = [7]
    new_library.books[Book(Author('Vytautas Mačernis'), 'Žmogaus Apnuoginta Širdis', 1980, Poetry())] = [8]
    new_library.books[Book(Author('Judita Vaičiūnaitė'), 'Pavasario Akvarelės', 1985, Poetry())] = [9]

    new_library.books[Book(Author('Vytautas Petkevičius'), 'Apie Viską ir Apie Nieko', 1972, Detective())] = [7]
    new_library.books[Book(Author('Rimantas Šavelis'), 'Šešėlių Žaidimas', 1978, Detective())] = [8]
    new_library.books[Book(Author('Algimantas Čekuolis'), 'Kryžkelės', 1980, Detective())] = [9]
    new_library.books[Book(Author('Vytautas Bubnys'), 'Alkana Žemė', 1982, Detective())] = [6]
    new_library.books[Book(Author('Rimantas Šavelis'), 'Mėnulio Šviesa', 1984, Detective())] = [7]
    new_library.books[Book(Author('Vytautas Petkevičius'), 'Dienos ir Naktys', 1986, Detective())] = [8]
    new_library.books[Book(Author('Algimantas Čekuolis'), 'Paskutinis Šūvis', 1989, Detective())] = [9]

    # add users

    new_library.users[User('Admin')] = [Librarian(), 'very_strong_password']
    new_library.users[User('Marina')] = [Librarian(), '1234']

    new_library.users[User('01')] = [Customer(), '0000']
    new_library.users[User('02')] = [Customer(), 'random']
    new_library.users[User('03')] = [Customer(), '23.14']
    new_library.users[User('04')] = [Customer(), '5888']
    new_library.users[User('05')] = [Customer(), 'kaka\n\r']

    # add boking records

    new_library.booking_records.append(BookingRecord(1, Borrow(), '01', Book(Author('Algimantas Čekuolis'), 'Kryžkelės', 1980, Detective())))
    new_library.booking_records[0].created_on = datetime.datetime.strptime("2024-10-01", "%Y-%m-%d")
    new_library.booking_records.append(BookingRecord(2, Borrow(), '01', Book(Author('Kazys Boruta'), 'Baltaragio malūnas', 1945, Epic())))
    new_library.booking_records[1].created_on = datetime.datetime.strptime("2024-10-05", "%Y-%m-%d")
    new_library.booking_records.append(BookingRecord(3, Borrow(), '02', Book(Author('Kazys Boruta'), 'Baltaragio malūnas', 1945, Epic())))
    new_library.booking_records[2].created_on = datetime.datetime.strptime("2024-10-09", "%Y-%m-%d")

    return new_library
