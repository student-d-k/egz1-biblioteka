
import sys
import datetime
import streamlit as st
from pathlib import Path

from classes.library import *
from data.def_library import *

library = None

# bandom nuskaityti biblioteka
# jeigu nepavyksta - sukuriam pre-defined

LIBRARY_FILE_NAME = 'library.dat'
LIBRARY_FOLDER_NAME = 'data'
LIBRARY_FULL_FILE_NAME = os.path.join(Path(__file__).resolve().parent, LIBRARY_FOLDER_NAME, LIBRARY_FILE_NAME)

try:

    with open(LIBRARY_FULL_FILE_NAME, 'rb') as f:
        library = pickle.load(f)

except IOError as e:
    print(e)

else:
    print('Biblioteka nuskaityta.')

finally:

    if library is None:
        library = create_default_library()
        print('Skurta nauja biblioteka.')


# filter_books = [e for e in filter(lambda book: book.year_of_release == 1980, library.books)]

# print(filter_books)

# filter_books = [e.book for e in filter(lambda br: (datetime.datetime.now()-br.created_on).days > BOOK_BORROW_MAX_DAYS, library.booking_records)]

# print(filter_books)

# print(library.books)
# print(library.users)
# print(library.booking_records)
# print()
# print(filter_books)
# print()

# add_book_to_library(library, Customer(), Book(Author('Kazys Boruta'), 'Baltaragio malūnas', 1945, Epic()))
# add_book_to_library(library, Librarian(), Book(Author('Kazys Boruta'), 'Baltaragio malūnas', 1945, Epic()))

# delete_book_from_library(library, Librarian(), 
#                          filter_function=lambda book: book == Book(Author('Kazys Boruta'), 'Baltaragio malūnas', 1945, Epic()))

# print()
# print(library.books)
# print(library.booking_records)

# delete_book_from_library(library, Librarian(), 
#                          filter_function=lambda book: book.year_of_release < 1970)

borrow_book_from_library(library, Customer(), '01', Book(Author('Kazys Boruta'), 'Baltaragio malūnas', 1945, Epic()))

borrow_book_from_library(library, Customer(), '01', Book(Author('Algimantas Čekuolis'), 'Kryžkelės', 1980, Detective()))

borrow_book_from_library(library, Customer(), '02', Book(Author('Algimantas Čekuolis'), 'Kryžkelės', 1980, Detective()))

borrow_book_from_library(library, Customer(), '03', Book(Author('Antanas Baranauskas'), 'Anykščių šilelis', 1905, Fiction()))

borrow_book_from_library(library, Customer(), '04', Book(Author('Antanas Baranauskas'), 'Anykščių šilelis', 1905, Fiction()))

# print()
# print(library.books)
for br in library.booking_records:
    print(br)

# UI

def validate_text_input(input_text):
    if not input_text.strip():
        return False
    return True


st.title('Library Management System')

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'current_role' not in st.session_state:
    st.session_state.current_role = None

if 'add_new_book_pressed' not in st.session_state:
    st.session_state.add_new_book_pressed = False


def handle_login():

    c1, c2, c3 = st.columns(3)
    with c1:
        user_name = st.text_input('User name')
    with c2:
        password = st.text_input('Password', type='password')
    with c3:
        if st.button('Login'):
            user = next((user for user in library.users if user.id == user_name), None)
            if user is None:
                st.write('unknown user')
            else:
                if library.users[user][1] == password:
                    st.session_state.current_user = user
                    st.session_state.current_role = library.users[user][0]
                    st.success(f'login successful as {st.session_state.current_role}')
                else:
                    st.write('incorrect password')


def handle_new_book():

    author_name = st.text_input('Author name')

    book_title = st.text_input('Book title')

    book_genre_str = st.radio('Select a genre', library.genres, format_func=str)

    year_of_release = st.number_input('Year of release', min_value=1900, max_value=2050, value=2024, step=1, format='%d')

    if st.button('Add', key='add_new_book_2'):

        if not validate_text_input(author_name):
            st.warning('Please enter a valid author name input')
            return
        if not validate_text_input(book_title):
            st.warning('Please enter a valid book title')
            return

        match book_genre_str:
            case 'Poezija':
                book_genre = Poetry()
            case 'Epas':
                book_genre = Epic()
            case 'Grožinė literatūra':
                book_genre = Fiction()
            case 'Pasaka':
                book_genre = Story()
            case 'Vaikiška literatūra':
                book_genre = Children()
            case 'Detektyvas':
                book_genre = Detective()
            case _:
                book_genre = None

        new_book = Book(Author(author_name), book_title, year_of_release, book_genre)
        add_book_to_library(library, Librarian(), new_book)

        st.write(book_genre_str)
        st.write(book_genre)
        st.success('New book added to library')

    if st.button('Back', key='back_2'):

        st.session_state.add_new_book_pressed = False


def handle_main():

    # list library books based on filter

    col1, col2 = st.columns([2, 1])

    with col1:

        # customer functionality

        c1, c2, c3 = st.columns(3)

        # paieskos kriterijai

        with c1:

            year_from = st.number_input('Year from', min_value=1900, max_value=2050, value=1900, step=1, format='%d')
            year_until = st.number_input('Year until', min_value=1900, max_value=2050, value=2050, step=1, format='%d')
            search_str = st.text_input('Search', value='*').lower()

        with c2:

            filter_overdued = st.checkbox('Overdued')
            # filter_in_library = st.checkbox('In library')
            # filter_booked = st.checkbox('Booked')
        
        with c3:

            # mano pasiimtos knygos funkcionalumas

            if st.button('My bookings'):

                my_bookings = [e.book for e in \
                        filter(lambda br: br.user_id == st.session_state.current_user.id, \
                        library.booking_records)]
                
                for e in my_bookings:
                    st.write(e)

            # pasiskolinti knyga funkcionalumas

            if st.session_state.current_role.can_borrow_book():

                delayed_books = [e.book for e in \
                        filter(lambda br: br.user_id == st.session_state.current_user.id and \
                                          (datetime.datetime.now()-br.created_on).days > BOOK_BORROW_MAX_DAYS, \
                        library.booking_records)]
                if len(delayed_books) > 0:
                    st.error('Jūs turite laiku negrąžintų knygų.')
                else:
                    if st.button('Make booking filtered books'):

                        if search_str == '*':
                            filter_books_0 = [book for book in library.books if year_from <= book.year_of_release <= year_until]

                        else:        
                            filter_books_0 = [
                                book for book in library.books
                                if year_from <= book.year_of_release <= year_until
                                and (search_str in book.author.author_name.lower() or search_str in book.caption.lower())
                            ]

                        if filter_overdued:
                            overdued_books = [e.book for e in filter(lambda br: (datetime.datetime.now()-br.created_on).days > BOOK_BORROW_MAX_DAYS, library.booking_records)]
                            filter_books = [item for item in filter_books_0 if item in overdued_books]
                        else:
                            filter_books = filter_books_0

                        if len(filter_books) > 1:
                            st.warning(f'You can borrow only 1 book at a time')
                        elif len(filter_books) == 0:
                            st.warning(f'No books in list')
                        else:
                            my_bookings = [e.book for e in \
                                filter(lambda br: br.user_id == st.session_state.current_user.id, \
                                library.booking_records)]
                            for book in filter_books:
                                if book in my_bookings:
                                    st.warning('You already have booked this book')
                                else:
                                    borrow_book_from_library(library, Customer(), st.session_state.current_user.id, book)
                                    st.success(f'Book {book} borrowed')

            # librarian functionality - add book

            if st.session_state.current_role.can_add_book():

                if st.button('Add new book', key='add_new_book_1'):
                    st.session_state.add_new_book_pressed = True

            # librarian functionality - delete book

            if st.session_state.current_role.can_delete_book():

                if st.button('Delete filtered books', key='delete_filtered_books_1'):

                    if search_str == '*':
                        filter_books_0 = [book for book in library.books if year_from <= book.year_of_release <= year_until]

                    else:        
                        filter_books_0 = [
                            book for book in library.books
                            if year_from <= book.year_of_release <= year_until
                            and (search_str in book.author.author_name.lower() or search_str in book.caption.lower())
                        ]

                    if filter_overdued:
                        overdued_books = [e.book for e in filter(lambda br: (datetime.datetime.now()-br.created_on).days > BOOK_BORROW_MAX_DAYS, library.booking_records)]
                        filter_books = [item for item in filter_books_0 if item in overdued_books]
                    else:
                        filter_books = filter_books_0

                    for b in filter_books:
                        delete_book_from_library(library, Librarian(), filter_function=lambda book: book == b)
                        st.success(f'Book {b} deleted')

                    st.write(f'Total: {len(filter_books)} book(s) deleted')

            # librarian functionality - list users

            if st.session_state.current_role.can_delete_book(): # reikia kitokio metodo

                if st.button('List users'):
                    for user in library.users:
                        st.write(f'id: {user}, role: {library.users[user][0]}, password: {library.users[user][1]}')
                        # st.write(library.users[user])

            # refresh button

            if st.button('Refresh'):
                pass

        # sudarom atfiltruotu knygu sarasa

        if search_str == '*':
            filter_books_0 = [book for book in library.books if year_from <= book.year_of_release <= year_until]

        else:        
            filter_books_0 = [
                book for book in library.books
                if year_from <= book.year_of_release <= year_until
                and (search_str in book.author.author_name.lower() or search_str in book.caption.lower())
            ]

        if filter_overdued:
            overdued_books = [e.book for e in filter(lambda br: (datetime.datetime.now()-br.created_on).days > BOOK_BORROW_MAX_DAYS, library.booking_records)]
            filter_books = [item for item in filter_books_0 if item in overdued_books]
        else:
            filter_books = filter_books_0

        for book in filter_books:
            # st.write(f'{book} [balance: {library.books[book][0]}]')
            st.write(book)

        st.write(f'Total: {len(filter_books)} book(s)')


if st.session_state.current_user is None:

    handle_login()

else:

    st.write(f'current user: {st.session_state.current_user} ({st.session_state.current_role})')
    
    if st.button('Logoff'):
        st.session_state.current_user = None
        st.session_state.current_role = None
        st.write('logged off')

    elif st.session_state.add_new_book_pressed == True:

        handle_new_book()

    else:

        handle_main()

# pries baigiant programa issaugom biblioteka su pakeitimais

try:

    with open(LIBRARY_FULL_FILE_NAME, 'wb') as f:
        pickle.dump(library, f)

    print('Biblioteka išsaugota.')

except IOError as e:
    print(e)
