import codecs
import re
import os

'''
EXTRACT_UTILS.PY

Utility methods for EXTRACT.PY
'''


def get_lines_from_file(filename):
    """
    Returns a list of all lines (as strings) that make up the file at the given file path.

    :param filename: The path of the file to open
    :return: A list of all lines in the file
    """

    # If the file name contains '-8' or '-0', it should be decoded as ISO-8859-1 instead of UTF-8
    # as long as a UTF-8 version cannot be found
    if bool(re.search(r'-\d\.txt', filename)):
        modded_filename = re.sub(r'-\d\.txt', r'.txt', filename)
        if not os.path.isfile(modded_filename):
            f = codecs.open(filename, 'r', 'iso-8859-1')
        else:
            return None
    else:
        f = codecs.open(filename, 'r', 'utf-8')

    # Attempt to read and split the file
    try:
        file_data = f.readlines()
    # If we assumed it was UTF-8, but we encounter a UnicodeDecodeError, try again with ISO-8859-1
    except UnicodeDecodeError:
        f.close()
        f = codecs.open(filename, 'r', 'iso-8859-1')
        file_data = f.readlines()

    f.close()

    return file_data


def extract_authors(author_line):
    """
    Takes the given line that presumably contains an author's name, and extract
    all authors from it, returning a list of all authors found

    :param author_line: String to extract authors from
    :return: A list containing all found authors
    """
    authors = []

    # Remove the author tag from the line
    author_line = str(author_line).replace("Author: ", "")
    # Remove random symbols
    author_line = re.sub(r'[\[\]]', r'', author_line)
    # Remove any content in parentheses
    author_line = re.sub(r'\((.*)\)', r'', author_line)
    # Remove component that starts with "Somethinged by" or with "Something:"
    author_line = re.sub(r'(.*by|.*:) (.*)', r'\2', author_line)
    # Remove spaces between initials, just for consistency (for 3-part initials)
    author_line = re.sub(r'([A-Z])\. ([A-Z])\. ([A-Z])\.', r'\1.\2.\3.', author_line)
    # Remove spaces between initials, just for consistency (for 2-part initials)
    author_line = re.sub(r'([A-Z])\. ([A-Z])\.', r'\1.\2.', author_line)
    # Remove any commas before junior or senior identifiers
    author_line = re.sub(r', [JjSs]r\.', r' Jr.', author_line)

    # If the line contains any "and"s, split by them to get list of separate authors
    for and_split in author_line.split(" and "):

        # Rearrange LastName, FirstName arrangements
        and_split = re.sub(r'^(\w+), (\w+)\s*$', r'\2 \1', and_split)
        # If the line contains any commas, split by them to get list of separate authors
        for split_author in and_split.split(", "):
            # Remove any string-final commas and periods, as well as any quotes, and
            # any string-initial or string-final whitespace
            split_author = re.sub(r'\.$|\"|,\s*$|^\s+|\s+$', r'', split_author)
            # Append the author the author set
            authors.append(split_author)

    return authors


def extract_title(title_line):
    """
    Takes the given line that presumably contains a text's title, and extract
    the title from the line and returning the title found

    :param title_line: String to extract title from
    :return: String of the extracted title
    """
    title = str(title_line).replace("Title: ", "")
    # Remove any string-initial or string-final whitespace
    title = re.sub(r'^\s+|\s+$', r'', title)

    return title



