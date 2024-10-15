
import sys
import datetime
import streamlit as st
from pathlib import Path
import statistics
from statistics import mode

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
        user_name = st.text_input('User name').lower()
    with c2:
        password = st.text_input('Password', type='password')
    with c3:
        if st.button('Login'):
            user = next((user for user in library.users if user.id.lower() == user_name), None)
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
        add_book_to_library(library, new_book)

        # st.write(book_genre_str)
        # st.write(book_genre)
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
            year_to = st.number_input('Year to', min_value=1900, max_value=2050, value=2050, step=1, format='%d')
            search_str = st.text_input('Search', value='*').lower()

        with c2:

            flag_overdued = st.checkbox('Overdued')
            flag_available = st.checkbox('Available')
            flag_booked = st.checkbox('Booked')
        
        with c3:

            # mano pasiimtos knygos funkcionalumas

            if st.button('My bookings'):

                my_bookings = [e.book for e in \
                        filter(lambda br: br.user_id == st.session_state.current_user.id, \
                        library.booking_records)]
                
                if len(my_bookings) == 0:
                    st.warning('You have no bookings')
                else:
                    for e in my_bookings:
                        st.write(e)

            # grazinti knygas funkcionalumas

            if  st.button('Return books back'):

                my_bookings = [e.book for e in \
                        filter(lambda br: br.user_id == st.session_state.current_user.id, \
                        library.booking_records)]

                if len(my_bookings) == 0:
                    st.warning('You have no books to return')
                else:
                    s = borrow_book_from_library(library, st.session_state.current_user.id, my_bookings[0], True)
                    if s != '':
                        st.warning(s)
                    else:
                        st.success(f'Book {my_bookings[0]} returned')

            # pasiskolinti knyga funkcionalumas

            if st.session_state.current_role.can_borrow_book():

                delayed_books = [e.book for e in \
                        filter(lambda br: br.user_id == st.session_state.current_user.id and \
                                          (datetime.datetime.now()-br.created_on).days > BOOK_BORROW_MAX_DAYS, \
                        library.booking_records)]
                if len(delayed_books) > 0:
                    st.warning('Jūs turite laiku negrąžintų knygų.')
                else:
                    if st.button('Make booking filtered books'):

                        filter_books = get_books_by_filter(library, search_str, year_from, year_to, flag_overdued, flag_available, flag_booked)

                        if len(filter_books) > 1:
                            st.warning(f'You can borrow only 1 book at a time')
                        elif len(filter_books) == 0:
                            st.warning(f'No books in list')
                        else:
                            s = borrow_book_from_library(library, st.session_state.current_user.id, filter_books[0], False)
                            if s != '':
                                st.warning(s)
                            else:
                                st.success(f'Book {filter_books[0]} borrowed')

            # librarian functionality - add book

            if st.session_state.current_role.can_add_book():

                if st.button('Add new book', key='add_new_book_1'):
                    st.session_state.add_new_book_pressed = True

            # librarian functionality - delete book

            if st.session_state.current_role.can_delete_book():

                if st.button('Delete filtered books', key='delete_filtered_books_1'):

                    filter_books = get_books_by_filter(library, search_str, year_from, year_to, flag_overdued, flag_available, flag_booked)

                    for book in filter_books:
                        s = delete_book_from_library(library, book)
                        if s != '':
                            st.warning(s)
                        else:
                            st.success(f'Book {book} deleted')

                    st.write(f'Total: {len(filter_books)} book(s) deleted')

            # librarian functionality - statistika

            if st.session_state.current_role.can_delete_book(): # reikia kitokio metodo

                if st.button('Statistics'):

                    genre_count = Counter()

                    for book in library.books.keys():
                        genre_count[book.genre] += 1

                    most_popular_genre = genre_count.most_common(1)[0]
                    st.write(f"The most popular genre is {most_popular_genre[0]} with {most_popular_genre[1]} books.")                    
                    # st.write(len(library.booking_records_history))

            # librarian functionality - list users

            if st.session_state.current_role.can_delete_book(): # reikia kitokio metodo

                if st.button('List users'):
                    for user in library.users:
                        st.write(f'id: {user}, role: {library.users[user][0]}, password: {library.users[user][1]}')
                        # st.write(library.users[user])

            # refresh button

            if st.button('Refresh'):
                pass

        # isvedam atfiltruotu knygu sarasa

        filter_books = get_books_by_filter(library, search_str, year_from, year_to, flag_overdued, flag_available, flag_booked)

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
