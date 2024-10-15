
pradziai:
    poetry shell
    poetry install

to run:
    streamlit run .\egz1_biblioteka\main.py

users list to login:
    user (librarian): Admin, password: x
    user (librarian): Marina, password: x
    user (customer): 01, password: x
    user (customer): 02, password: x
    user (customer): 03, password: x
    user (customer): 04, password: x
    user (customer): 05, password: x

comments:

    failas db_struktura.drawio buvo mintis duomenų bazės ir saugoti duomenis ne faile, o db. Bet pagalvojau, kokį sqlite ne visi turi, azure neturiu account nemokamo, o ir su streamlite.auth pražaidžiau pusę dienos, pamačiau, kad nespėsiu.