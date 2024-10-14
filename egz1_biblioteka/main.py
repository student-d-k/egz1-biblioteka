
import sys
import datetime
import streamlit as st

from classes.library import *

BOOK_BORROW_MAX_DAYS = 14

library = None

# bandom nuskaityti biblioteka
# jeigu nepavyksta, sukuriam pre-defined

LIBRARY_FILE_NAME = 'library.dat'
LIBRARY_FOLDER_NAME = 'data'
LIBRARY_FULL_FILE_NAME = os.path.join(Path(__file__).resolve().parent, LIBRARY_FOLDER_NAME, LIBRARY_FILE_NAME)

try:

    with open(LIBRARY_FULL_FILE_NAME, 'rb') as f:
        library = pickle.load(f)

except IOError as e:

    print(e)

    # sys.exit

else:
    print('Biblioteka nuskaityta.')

finally:

    if library is None:

        library = Library()

        library.books[Book(Author('Kazys Boruta'), 'Baltaragio malūnas', 1945, Epic())] = [4]
        library.books[Book(Author('Vincas Krėvė-Mickevičius'), 'Šiaudinėj pastogėj', 1935, Epic())] = [3]

        library.books[Book(Author('Antanas Baranauskas'), 'Anykščių šilelis', 1905, Fiction())] = [1]
        library.books[Book(Author('Antanas Baranauskas'), 'Anykščių šilelis', 2017, Fiction())] = [5]

        library.books[Book(Author('Salomėja Nėris'), 'Eglė žalčių karalienė', 1940, Story())] = [8]

        library.books[Book(Author('Eduardas Mieželaitis'), 'Zuikis Puikis', 1956, Children())] = [2]
        library.books[Book(Author('Vytautas V. Landsbergis'), 'Arklio Dominyko meilė', 1985, Children())] = [1]
        library.books[Book(Author('Antanas Vienuolis'), 'Paskenduolė', 1928, Children())] = [5]
        library.books[Book(Author('Jonas Biliūnas'), 'Laimės žiburys', 1905, Children())] = [6]

        library.books[Book(Author('Vytautas Petkevičius'), 'Molio Motiejus', 1978, Poetry())] = [1]
        library.books[Book(Author('Salomėja Nėris'), 'Eglė žalčių karalienė', 2019, Poetry())] = [3]
        library.books[Book(Author('Salomėja Nėris'), 'Poetry Collections', 1945, Poetry())] = [8]
        library.books[Book(Author('Eduardas Mieželaitis'), 'Mano Draugas', 1954, Poetry())] = [7]
        library.books[Book(Author('Justinas Marcinkevičius'), 'Mindaugas', 1968, Poetry())] = [9]
        library.books[Book(Author('Sigitas Geda'), 'Strazdas', 1972, Poetry())] = [8]
        library.books[Book(Author('Marcelijus Martinaitis'), 'Kukučio Baladės', 1977, Poetry())] = [7]
        library.books[Book(Author('Vytautas Mačernis'), 'Žmogaus Apnuoginta Širdis', 1980, Poetry())] = [8]
        library.books[Book(Author('Judita Vaičiūnaitė'), 'Pavasario Akvarelės', 1985, Poetry())] = [9]

        library.books[Book(Author('Vytautas Petkevičius'), 'Apie Viską ir Apie Nieko', 1972, Detective())] = [7]
        library.books[Book(Author('Rimantas Šavelis'), 'Šešėlių Žaidimas', 1978, Detective())] = [8]
        library.books[Book(Author('Algimantas Čekuolis'), 'Kryžkelės', 1980, Detective())] = [9]
        library.books[Book(Author('Vytautas Bubnys'), 'Alkana Žemė', 1982, Detective())] = [6]
        library.books[Book(Author('Rimantas Šavelis'), 'Mėnulio Šviesa', 1984, Detective())] = [7]
        library.books[Book(Author('Vytautas Petkevičius'), 'Dienos ir Naktys', 1986, Detective())] = [8]
        library.books[Book(Author('Algimantas Čekuolis'), 'Paskutinis Šūvis', 1989, Detective())] = [9]

        library.users[User('Admin')] = [Librarian(), 'very_strong_password']
        library.users[User('Marina')] = [Librarian(), '1234']

        library.users[User('01')] = [Customer(), '0000']
        library.users[User('02')] = [Customer(), 'random']
        library.users[User('03')] = [Customer(), 23.14]
        library.users[User('04')] = [Customer(), 5888]
        library.users[User('05')] = [Customer(), 'kaka\n\r']

        library.booking_records.append(BookingRecord(1, Borrow(), '01', Book(Author('Algimantas Čekuolis'), 'Kryžkelės', 1980, Detective())))
        library.booking_records[0].created_on = datetime.datetime.strptime("2024-10-01", "%Y-%m-%d")
        library.booking_records.append(BookingRecord(2, Borrow(), '01', Book(Author('Kazys Boruta'), 'Baltaragio malūnas', 1945, Epic())))
        library.booking_records[1].created_on = datetime.datetime.strptime("2024-10-05", "%Y-%m-%d")
        library.booking_records.append(BookingRecord(3, Borrow(), '02', Book(Author('Kazys Boruta'), 'Baltaragio malūnas', 1945, Epic())))
        library.booking_records[2].created_on = datetime.datetime.strptime("2024-10-09", "%Y-%m-%d")

        print('Skurta nauja biblioteka.')


# 1 prideti knyga i biblioteka

def add_book_to_library(library: Library, role: Role, book: Book):
    """
    Adds books to library.

    Parameters:
    library (Library): The library where to add the book.
    role (Role): The role of the person attempting to add the book.
    book (Book): The book to be added.
    """

    try:

        if role.can_add_book():

            if book in library.books:
                library.books[book][0] += 1
            else:
                library.books[book] = 1

            print(f'Pridėjau knygą: "{book}".')

        else:
            print('Jūs neturite teisių pridėti knygos.')

    except Exception as e:

        print(e)

# 2 pasalinti senas knygas is bibliotekos

def delete_book_from_library(library: Library, role: Role, filter_function: callable):
    """
    Deletes books from the library based on a filter function.

    Parameters:
    library (Library): The library from which to delete books.
    role (Role): The role of the person attempting to delete the book.
    filter (callable): A function that takes a book and returns True if the book should be deleted.
    """

    try:

        if not role.can_delete_book():
            print('Jūs neturite teisių ištrinti knygos.')
            return

        delete_list_books = [e for e in filter(filter_function, library.books)]

        for book in delete_list_books:

            library.books.pop(book)
            print(f'Ištryniau knygą "{str(book)}"')

            delete_list_booking_records = [(i, br) for i, br in enumerate(library.booking_records) if br.book == book]
            delete_list_booking_records.sort(reverse=True, key=lambda x: x[0])

            for i, br in delete_list_booking_records:
                r = library.booking_records.pop(i)
                print(f'Ištryniau įrašą {str(r)}')

    except Exception as e:

        print(e)

# 3, 8 pasiimti knyga issinesimui

def borrow_book_from_library(library: Library, role: Role, user_id: User, book: Book):
    """
    Borrows book from the library based on a customer.

    Parameters:
    library (Library): The library from which to borrow book.
    role (Role): The role of the person attempting to borrow the book.
    user (User): The user attempting to borrow the book.
    book (Book): The book to be borrowed.
    """

    try:

        if not role.can_borrow_book(): 
            print('Jūs neturite teisių išsinuomoti knygos.')
            return

        if not book in library.books:
            print('Bibliotekoje nėra tokios knygos.')
            return

        if library.books[book] == 0:
            print('Visos knygos išnuomotos.')
            return

        delayed_books = [e.book for e in \
                        filter(lambda br: br.user_id == user_id and \
                                          (datetime.datetime.now()-br.created_on).days > BOOK_BORROW_MAX_DAYS, \
                        library.booking_records)]

        if len(delayed_books) > 0:
            print('Jūs turite laiku negrąžintų knygų.')
            return

        already_have_booking = [e.book for e in filter(lambda br: br.user_id == user_id and br.book == book, library.booking_records)]

        if len(already_have_booking) > 0:
            print('Jūs jau esate pasiėmęs šitą knygą.')
            return

        # pridedam irasa

        library.booking_records.append(BookingRecord(len(library.booking_records)+1, Borrow(), user_id, book))

        print(library.booking_records[-1])

    except Exception as e:

        print(e)

# 4, 5, 6, 7 ieskoti knygu pagal pavadinima arba autoriu arba pagal velavima

filter_books = [e for e in filter(lambda book: book.year_of_release == 1980, library.books)]

print(filter_books)

filter_books = [e.book for e in filter(lambda br: (datetime.datetime.now()-br.created_on).days > BOOK_BORROW_MAX_DAYS, library.booking_records)]

print(filter_books)

# print(library.books)
# print(library.users)
# print(library.booking_records)
# print()
# print(filter_books)
# print()

add_book_to_library(library, Customer(), Book(Author('Kazys Boruta'), 'Baltaragio malūnas', 1945, Epic()))
add_book_to_library(library, Librarian(), Book(Author('Kazys Boruta'), 'Baltaragio malūnas', 1945, Epic()))

delete_book_from_library(library, Librarian(), 
                         filter_function=lambda book: book == Book(Author('Kazys Boruta'), 'Baltaragio malūnas', 1945, Epic()))

# print()
# print(library.books)
# print(library.booking_records)

delete_book_from_library(library, Librarian(), 
                         filter_function=lambda book: book.year_of_release < 1970)

borrow_book_from_library(library, Customer(), '01', Book(Author('Kazys Boruta'), 'Baltaragio malūnas', 1945, Epic()))

borrow_book_from_library(library, Customer(), '01', Book(Author('Algimantas Čekuolis'), 'Kryžkelės', 1980, Detective()))

borrow_book_from_library(library, Customer(), '02', Book(Author('Algimantas Čekuolis'), 'Kryžkelės', 1980, Detective()))

borrow_book_from_library(library, Customer(), '03', Book(Author('Antanas Baranauskas'), 'Anykščių šilelis', 1905, Fiction()))

borrow_book_from_library(library, Customer(), '04', Book(Author('Antanas Baranauskas'), 'Anykščių šilelis', 1905, Fiction()))

# print()
# print(library.books)
for br in library.booking_records:
    print(br)

# pries baigiant programa issaugom biblioteka su pakeitimais

try:

    with open(LIBRARY_FULL_FILE_NAME, 'wb') as f:
        pickle.dump(library, f)

    print('Biblioteka išsaugota.')

except IOError as e:
    print(e)
