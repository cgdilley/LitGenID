import re                       # For handling regexes
import ast                      # For parsing lists from strings
import csv                      # For processing CSV files
from fuzzywuzzy import fuzz     # For finding inexact string matches
import os                       # For file management operations
import errno                    # For error handling

'''
PROCESSRESULTS_UTILS.PY

Utility methods for PROCESSRESULTS.PY and ASSEMBLECORPUS.PY
'''


class TextData:
    title = ""
    authors = []
    path = ""
    labels = set()

    def __init__(self, title_, authors_, path_, labels_):
        self.title = title_
        self.authors = authors_
        self.path = path_
        self.labels = labels_

    def __str__(self, *args, **kwargs):
        return "({}, {}, {}, {})".format(self.title, self.authors, self.path, self.labels)


def extract_data_from_row(row):
    """
    Extracts title, author, and path information from the given list extracted
    directly from a csv file

    :param row: List containing elements extracted from a csv file's row
    :return: A TextData object representing the extracted data
    """

    # Extract info from the row list
    title = row[0]
    authors = row[1]
    path = row[2]
    labels = row[3]

    # Ignore the column header line
    if title == "TITLE":
        return None

    # Remove any surrounding quotes from the fields
    title = re.sub(r'^"|"$|^\'|\'$', r'', title)
    authors = re.sub(r'^"|"$|^\'|\'$', r'', authors)
    path = re.sub(r'^"|"$|^\'|\'$', r'', path)
    labels = re.sub(r'^"|"$|^\'|\'$', r'', labels)

    try:
        # Attempt to convert the authors field to a python list
        authors_list = ast.literal_eval(authors)
        # Attempt to convert the labels field to a python set
        labels_set = set(ast.literal_eval(labels))
        # Create the new TextData object
        obj = TextData(title, authors_list, path, labels_set)
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


def match_author_list(author_list1, author_list2):
    """
    Determines whether at least one author from the first list matches at least one author from the second list

    :param author_list1: First list of authors to compare
    :param author_list2: Second list of authors to compare
    :return: Returns True if there was at least one author match, False otherwise
    """
    for author1 in author_list1:
        for author2 in author_list2:
            if fuzz.token_sort_ratio(author1, author2) >= 50:
                return True

    return False


def merge_data(data1, data2):
    """
    Merges the two given lists of TextData, eliminating any duplicate title+author combos as well as any duplicate
    file paths.  Genre sets of duplicates are merged before removal.

    :param data1: First TextData list to merge
    :param data2: Second TextData list to merge
    :return: The merged data list
    """

    # Initialize data dictionary, which will contain key-value pairs with the book's title as the unique key, and
    # a list of TextData with that title as the value (elements of this list will have unique authors).
    title_dict = dict()
    # Initialize data dictionary, which will contain key-value pairs with the Gutenberg text path as the unique key, and
    # the TextData object as a value (ensures that the same text file is not referenced twice).
    data_dict = dict()

    # Iterate through all TextData from the Gutenberg-labelled set
    for datum in data1:
        # If the text file is not already referenced in the data set, add it to the data set
        if datum.path not in data_dict:

            # If the title is not found in the title set
            if datum.title not in title_dict:
                # Add TextData to data set
                data_dict[datum.path] = datum
                # Add the TextData to the title set
                title_dict[datum.title] = [datum]
            # Otherwise, if the title has already been found (but with a different file path)
            else:
                match_found = False
                # Iterate through all TextData associated with the title
                for title_elem in title_dict[datum.title]:
                    # If there is also an author match
                    if match_author_list(title_elem.authors, datum.authors):
                        # Merge the labels of the matched TextData in the data set with this data element
                        data_dict[title_elem.path].labels |= datum.labels
                        match_found = True
                # If no author match was found
                if not match_found:
                    # Add this data element to the list in the title set with the matching title
                    title_dict[datum.title].append(datum)
                    # Add this data element to the data set
                    data_dict[datum.path] = datum

        # If the text file is already referenced in the data set, then union their sets of genres
        else:
            data_dict[datum.path].labels |= datum.labels

    # Iterate through all TextData from the IBList-labelled set (Copy-paste of above code)
    for datum in data2:
        # If the text file is not already referenced in the data set, add it to the data set
        if datum.path not in data_dict:

            # If the title is not found in the title set
            if datum.title not in title_dict:
                # Add TextData to data set
                data_dict[datum.path] = datum
                # Add the TextData to the title set
                title_dict[datum.title] = [datum]
            # Otherwise, if the title has already been found (but with a different file path)
            else:
                match_found = False
                # Iterate through all TextData associated with the title
                for title_elem in title_dict[datum.title]:
                    # If there is also an author match
                    if match_author_list(title_elem.authors, datum.authors):
                        # Merge the labels of the matched TextData in the data set with this data element
                        data_dict[title_elem.path].labels |= datum.labels
                        match_found = True
                # If no author match was found
                if not match_found:
                    # Add this data element to the list in the title set with the matching title
                    title_dict[datum.title].append(datum)
                    # Add this data element to the data set
                    data_dict[datum.path] = datum

                    # If the text file is already referenced in the data set, then union their sets of genres
        else:
            data_dict[datum.path].labels |= datum.labels

    # Return the value list of the data set
    return data_dict.values()


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def format_genre_path(genre):
    return "./CORPUS/" + re.sub(r'\s|and', r'', genre) + "/"

