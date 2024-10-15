
import sys
import datetime
import streamlit as st
from pathlib import Path
import statistics
from statistics import mode
import pickle

from egz1_biblioteka.classes.library import *
from egz1_biblioteka.data.def_library import *

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'current_role' not in st.session_state:
    st.session_state.current_role = None

if 'add_new_book_pressed' not in st.session_state:
    st.session_state.add_new_book_pressed = False

if 'any_changes_to_library' not in st.session_state:
    st.session_state.any_changes_to_library = False

if 'library' not in st.session_state:
    st.session_state.library = None


# bandom nuskaityti biblioteka
# jeigu nepavyksta - sukuriam pre-defined

LIBRARY_FILE_NAME = 'library.dat'
LIBRARY_FOLDER_NAME = 'data'
LIBRARY_FULL_FILE_NAME = os.path.join(Path(__file__).resolve().parent, LIBRARY_FOLDER_NAME, LIBRARY_FILE_NAME)

try:

    if st.session_state.library is None:

        with open(LIBRARY_FULL_FILE_NAME, 'rb') as f:
            st.session_state.library = pickle.load(f)
            st.session_state.any_changes_to_library = True

        print('Biblioteka nuskaityta.')

except IOError as e:
    print(e)

finally:

    if st.session_state.library is None:
        st.session_state.library = create_default_library()
        st.session_state.any_changes_to_library = True
        print('Skurta nauja biblioteka.')


# UI

def validate_text_input(input_text):
    if not input_text.strip():
        return False
    return True


st.title('Library Management System')


def handle_login():

    c1, c2, c3 = st.columns(3)
    with c1:
        user_name = st.text_input('User name').lower()
    with c2:
        password = st.text_input('Password', type='password')
    with c3:
        if st.button('Login'):
            user = next((user for user in st.session_state.library.users if user.id.lower() == user_name), None)
            if user is None:
                st.write('unknown user')
            else:
                if st.session_state.library.users[user][1] == password:
                    st.session_state.current_user = user
                    st.session_state.current_role = st.session_state.library.users[user][0]
                    st.success(f'login successful as {st.session_state.current_role}')
                    st.rerun()
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

        match str(book_genre_str):
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
        s =  add_book_to_library(st.session_state.library, new_book)
        if s == '':
            st.success('New book added to library')
            st.session_state.any_changes_to_library = True
        else:
            st.warning(s)

    if st.button('Back', key='back_2'):

        st.session_state.add_new_book_pressed = False
        st.rerun()


def handle_stat():

    # statistika is einamu ir istoriniu irasu

    d1 = {} # veluojancios knygos
    d2 = {} # zanru kiekis tarp isnuomotu knygu
    l3 = [] # knygos nuomos laikas

    # check past booking history

    for br in st.session_state.library.booking_records_history:

        if (br.returned_on - br.created_on).days > BOOK_BORROW_MAX_DAYS:
            if br.user_id in d1:
                d1[br.user_id] += 1
            else:
                d1[br.user_id] = 1

        if str(br.book.genre) in d2:
            d2[str(br.book.genre)] += 1
        else:
            d2[str(br.book.genre)] = 1

        l3.append((br.returned_on - br.created_on).days)

    # check current booking records

    for br in st.session_state.library.booking_records:

        if (datetime.datetime.now() - br.created_on).days > BOOK_BORROW_MAX_DAYS:
            if br.user_id in d1:
                d1[br.user_id] += 1
            else:
                d1[br.user_id] = 1

        if str(br.book.genre) in d2:
            d2[str(br.book.genre)] += 1
        else:
            d2[str(br.book.genre)] = 1

    # daugiausiai is bibliotekos knygu

    d4 = {} # zanru kiekis bibliotekoje

    for book in library.books:

        if str(book.genre) in d4:
            d4[str(book.genre)] += 1
        else:
            d4[str(book.genre)] = 1

    # isvedam statistika - veluojantys useriai

    if d1:
        max_overdued_books = max(d1.values())
        most_careless_users = [user_id for user_id, overdued_books in d1.items() if overdued_books == max_overdued_books]
        st.write(f"The most careless users are {most_careless_users} with {max_overdued_books} overdue books each")
    else:
        st.write("No careless users found.")

    # isvedam statistika - daugiausiai zanro knygu bibliotekoje

    if d4:
        max_genre_books = max(d4.values())
        most_popular_genre_in_library = [genre for genre, count in d4.items() if count == max_genre_books]
        st.write(f"The most popular genre in library is {most_popular_genre_in_library} with {max_genre_books} books")
    else:
        st.write("No books in library")

    # daugiausiai zanro knygu nuomojama

    if d2:
        max_genre_booked = max(d2.values())
        most_popular_genre_in_bookings = [genre for genre, count in d2.items() if count == max_genre_booked]
        st.write(f"The most popular genre in bookings is {most_popular_genre_in_bookings} with {max_genre_booked} books")
    else:
        st.write("No books booked")

    # vidutinis knygos nuomos laikas

    if l3:
        st.write(f"Average booking duration is {sum(l3) / len(l3):.1f} days")
    else:
        st.write("No books in booking history")


def handle_main():

    # list library books based on filter

    col1, col2 = st.columns([3, 1])

    with col1:

        # customer functionality

        c1, c2, c3 = st.columns(3)

        # paieskos kriterijai

        with c1:

            year_from = st.number_input('Year from', min_value=1900, max_value=2050, value=1900, step=1, format='%d')
            year_to = st.number_input('Year to', min_value=1900, max_value=2050, value=2050, step=1, format='%d')
            search_str = st.text_input('Search', value='*').lower()

        with c2:

            flag_overdued = st.checkbox('Overdued')
            flag_available = st.checkbox('Available')
            flag_booked = st.checkbox('Booked')
        
        with c3:

            if st.button('Refresh'):
                pass

            # mano pasiimtos knygos funkcionalumas

            if st.button('My bookings'):

                my_bookings = [e.book for e in \
                        filter(lambda br: br.user_id == st.session_state.current_user.id, \
                        st.session_state.library.booking_records)]
                
                if len(my_bookings) == 0:
                    st.warning('You have no bookings')
                else:
                    for e in my_bookings:
                        st.write(e)

            # grazinti knygas funkcionalumas

            if  st.button('Return books back'):

                my_bookings = [e.book for e in \
                        filter(lambda br: br.user_id == st.session_state.current_user.id, \
                        st.session_state.library.booking_records)]

                if len(my_bookings) == 0:
                    st.warning('You have no books to return')
                else:
                    s = borrow_book_from_library(st.session_state.library, st.session_state.current_user.id, my_bookings[0], True)
                    if s != '':
                        st.warning(s)
                    else:
                        st.session_state.any_changes_to_library = True
                        st.success(f'Book {my_bookings[0]} returned')

            # pasiskolinti knyga funkcionalumas

            if st.session_state.current_role.can_borrow_book():

                delayed_books = [e.book for e in \
                        filter(lambda br: br.user_id == st.session_state.current_user.id and \
                                            (datetime.datetime.now() - br.created_on).days > BOOK_BORROW_MAX_DAYS, \
                        st.session_state.library.booking_records)]
                if len(delayed_books) > 0:
                    st.warning('Jūs turite laiku negrąžintų knygų.')
                else:
                    if st.button('Make booking filtered books'):

                        filter_books = get_books_by_filter(st.session_state.library, search_str, year_from, year_to, flag_overdued, flag_available, flag_booked)

                        if len(filter_books) > 1:
                            st.warning(f'You can borrow only 1 book at a time')
                        elif len(filter_books) == 0:
                            st.warning(f'No books in list')
                        else:
                            s = borrow_book_from_library(st.session_state.library, st.session_state.current_user.id, filter_books[0], False)
                            if s != '':
                                st.warning(s)
                            else:
                                st.session_state.any_changes_to_library = True
                                st.success(f'Book {filter_books[0]} borrowed')

        # isvedam atfiltruotu knygu sarasa

        filter_books = get_books_by_filter(st.session_state.library, search_str, year_from, year_to, flag_overdued, flag_available, flag_booked)

        for book in filter_books:
            # st.write(f'{book} [balance: {library.books[book][0]}]')
            st.write(book)

        st.write(f'Total: {len(filter_books)} book(s)')

    with col2:

        # librarian functionality - add book

        if st.session_state.current_role.can_add_book():

            if st.button('Add new book', key='add_new_book_1'):
                st.session_state.add_new_book_pressed = True

        # librarian functionality - delete book

        if st.session_state.current_role.can_delete_book():

            if st.button('Delete filtered books', key='delete_filtered_books_1'):

                filter_books = get_books_by_filter(st.session_state.library, search_str, year_from, year_to, flag_overdued, flag_available, flag_booked)

                for book in filter_books:
                    s = delete_book_from_library(st.session_state.library, book)
                    if s != '':
                        st.warning(s)
                    else:
                        st.session_state.any_changes_to_library = True
                        st.success(f'Book {book} deleted')

                st.write(f'Total: {len(filter_books)} book(s) deleted')

        # librarian functionality - statistika

        if st.session_state.current_role.can_delete_book(): # reikia kitokio metodo

            if st.button('Statistics'):

                handle_stat()

        # librarian functionality - list users

        if st.session_state.current_role.can_delete_book(): # reikia kitokio metodo

            if st.button('List users'):
                for user in st.session_state.library.users:
                    st.write(f'id: {user}, role: {st.session_state.library.users[user][0]}, password: {st.session_state.library.users[user][1]}')
                    # st.write(st.session_state.library.users[user])


if st.session_state.current_user is None:

    handle_login()

else:

    st.write(f'current user: {st.session_state.current_user} ({st.session_state.current_role})')

    if st.button('Logoff'):
        st.session_state.current_user = None
        st.session_state.current_role = None
        st.write('logged off')
        st.rerun()

    elif st.session_state.add_new_book_pressed == True:

        handle_new_book()

    else:

        handle_main()


# pries baigiant programa issaugom biblioteka su pakeitimais

if st.session_state.any_changes_to_library:

    try:

        with open(LIBRARY_FULL_FILE_NAME, 'wb') as f:
            pickle.dump(st.session_state.library, f)

        st.session_state.any_changes_to_library = False
        print('Biblioteka išsaugota.')

    except IOError as e:
        print(e)
