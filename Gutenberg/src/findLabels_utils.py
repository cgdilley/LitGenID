import re                       # For handling regexes
import ast                      # For parsing lists from strings
import urllib.parse             # For parsing URL strings
from bs4 import BeautifulSoup   # For navigating HTML structure
import requests                 # For performing HTML requests
from fuzzywuzzy import fuzz     # For finding inexact string matches
import csv                      # For processing CSV files

'''
FINDLABELS_UTILS.PY

Utility methods for FINDURLS_IBLIST.PY, FINDLABELS_IBLIST.PY, and FINDLABELS_GUTEN.PY
'''


class TextData:
    title = ""
    authors = []
    path = ""
    labels = []
    url = ""

    def __init__(self, title_, authors_, path_):
        self.title = title_
        self.authors = authors_
        self.path = path_

    def __str__(self, *args, **kwargs):
        return "({}, {}, {})".format(self.title, self.authors, self.path)


def extract_data_from_row(row):
    """
    Extracts title, author, and path information from the given list extracted
    directly from a csv file

    :param row: List containing elements extracted from a csv file's row
    :return: A TextData object representing the extracted data
    """

    # Extract info.txt from the row list
    title = row[0]
    authors = row[1]
    path = row[2]
    # If this row contains a URL, extract it, otherwise leave as None
    url = None if len(row) <= 3 else row[3]

    # Ignore the column header line
    if title == "TITLE":
        return None

    # Remove any surrounding quotes from the fields
    title = re.sub(r'^"|"$|^\'|\'$', r'', title)
    authors = re.sub(r'^"|"$|^\'|\'$', r'', authors)
    path = re.sub(r'^"|"$|^\'|\'$', r'', path)

    try:
        # Attempt to convert the authors field to a python list
        authors_list = ast.literal_eval(authors)
        # Create the new TextData object
        obj = TextData(title, authors_list, path)
        if url is not None:
            obj.url = url
        return obj
    except ValueError as e:
        # If author string could not be converted to a list, report the error
        print(e)
        print("Text: " + str(authors))
        return None


def csv_to_text_data_list(csv_path):
    """
    Opens a CSV file at the given path, and extracts all elements from it as TextData objects, and returns a list
    of all extract TextData.

    :param csv_path: Path of the CSV file to open.
    :return: A list of TextData objects, or an empty list if the file does not exist.
    """

    data = []
    try:
        # Open csv file containing text data
        with open(csv_path, "r") as f:
            csv_reader = csv.reader(f)
            # Iterate through all data rows
            for row in csv_reader:
                datum = extract_data_from_row(row)
                if datum is not None:
                    data.append(datum)
    except FileNotFoundError:
        raise

    return data


def title_match(title1, title2):
    return fuzz.token_sort_ratio(title1, title2) >= 90


def author_match(author1, author2):
    return fuzz.token_sort_ratio(author1, author2) >= 50


def perform_iblist_search(search):
    """
    Performs a search query at iblist.com for the given text data

    :param search: TextData object containing title and author to search for
    :return: URL of the iblist page for the book, if a match was found.
             If no match was found, returns None.
    """
    # Get title and author from the given search TextData
    search_title = search.title
    search_author = search.authors[0]

    query = search_title + ", " + search_author

    # Construct the searching URL
    fields = {"item": query, "submit": "Search"}
    encoded_fields = urllib.parse.urlencode(fields)
    full_url = "http://www.iblist.com/search/search.php?" + encoded_fields

    # Perform the search request, and get the HTML result
    result_text = requests.get(full_url).text

    # Parse the HTML result
    result_soup = BeautifulSoup(result_text, 'lxml')

    # Look for <div> that contains results
    body = result_soup.find("div", class_="boxbody")

    # Iterate through all search results
    for list_item in body.find_all("li"):
        # Extract author and title tags
        title_tag = list_item.contents[0]
        author_tag = list_item.contents[2]

        # Get result author
        result_author = str(author_tag.contents[0])

        # Get result title
        result_title = str(title_tag.contents[0])
        # Remove year from result
        result_title = re.sub(r' \(.*\)$', r'', result_title)

        # If a result is a match, then return the URL for the book
        if title_match(result_title, search_title) and author_match(search_author, result_author):
            return title_tag['href']

    # If no matches were found after iterating through all results, return None
    return None


def extract_iblist_genres(book_url, match_genres):
    """
    Queries the given book url, and extracts the genre information from the returned html page.

    :param book_url: URL of the book to get genre information for
    :param match_genres: Set of genres to accept as valid
    :return: List of identified genres of the book at the given URL.  If the book was not identified as a novel,
            or none of its genres were in the given genre set, returns an empty list
    """

    result_text = requests.get(book_url).text

    result_soup = BeautifulSoup(result_text, 'lxml')

    novel_tag = result_soup.find("div", class_="boxbody").find("table").find("table").find("b").contents[1]

    if novel_tag != " [Novel]":
        return []

    genre_tag_list = result_soup.find("div", class_="boxbody").find(string="Genre:").parent.parent.find_all("a")

    genre_matches = []
    for genre_tag in genre_tag_list:
        genre = genre_tag.contents[0]
        if genre in match_genres:
            genre_matches.append(genre)

    return genre_matches
