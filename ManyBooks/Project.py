import requests


# create a list with the book name, url, and the author
def create_book_list(file_name, genre_list):
    i = 0
    # Create list containing book names and download link and author
    f = open(file_name)
    for lines in f:
        if i == 0:
            i += 1
        else:
            genre_list.append(lines.split('\t'))


# download books using request from manyboks.net
def download_books(genre_list):
    for i, j, k in genre_list:
        url = j
        i = i.replace(' ', '_')
        i += '.txt'
        print("downloading with requests")
        r = requests.get(url)
        with open(i, "wb") as code:
            code.write(r.content)
'''
adventure_list = []
create_book_list("Adventure_Books.txt", adventure_list)

fantasy_list = []
create_book_list("Fantasy_Books.txt", fantasy_list)

horror_list = []
create_book_list("Horror_Books.txt", horror_list)

romance_list = []
create_book_list("Romance_Books.txt", romance_list)
'''
scifi_list = []
create_book_list("Sci-Fi_Books.txt", scifi_list)
'''
western_list = []
create_book_list("Western_Books.txt", western_list)

# -------------------------------------------------------------------------------------------------------------------


download_books(adventure_list)

download_books(fantasy_list)

download_books(horror_list)

download_books(romance_list)
'''
download_books(scifi_list)
