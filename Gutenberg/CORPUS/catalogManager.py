import re                       # For handling regexes
import ast                      # For parsing lists from strings
import csv                      # For processing CSV files

'''
CATALOGMANAGER.PY

Contains the definition for the CatalogManager class, which allows one to load the catalog of the corpus, and perform
queries on the corpus data
'''


class CatalogManager:
    """
    Class for loading the catalog, and performing queries on it
    """
    titleIndex = dict()
    authorIndex = dict()
    pathIndex = dict()
    labelIndex = dict()
    
    def __init__(self):
        # Load the catalog csv file
        data = csv_to_text_data_list("./catalog.csv")

        # Build indices for all fields
        for datum in data:
            add_to_dict_list(self.titleIndex, datum.title, datum)
            for author in datum.authors:
                add_to_dict_list(self.authorIndex, author, datum)
            for path in datum.paths:
                add_to_dict_list(self.pathIndex, path, datum)
            for label in datum.labels:
                add_to_dict_list(self.labelIndex, label, datum)

    def title_query(self, title):
        """
        Get list of TextData with the given title
        :param title: Title to query for
        :return: List of results
        """
        return self.titleIndex[title]
    
    def author_query(self, author):
        """
        Get list of TextData with the given author
        :param author: Author to query for
        :return: List of results
        """
        return self.authorIndex[author]
    
    def path_query(self, path):
        """
        Get list of TextData with the given path
        :param path: Path to query for
        :return: List of results
        """
        return self.pathIndex[path]
    
    def label_query(self, label):
        """
        Get list of TextData with the given label
        :param label: Label to query for
        :return: List of results
        """
        return self.labelIndex[label]
        
        
def add_to_dict_list(dictionary, key, value):
    if key in dictionary:
        dictionary[key].append(value)
    else:
        dictionary[key] = [value]


class TextData:
    title = ""
    authors = []
    paths = []
    labels = set()

    def __init__(self, title_, authors_, paths_, labels_):
        self.title = title_
        self.authors = authors_
        self.paths = paths_
        self.labels = labels_

    def __str__(self, *args, **kwargs):
        return "({}, {}, {}, {})".format(self.title, self.authors, self.paths, self.labels)


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
    paths = row[2]
    labels = row[3]

    # Ignore the column header line
    if title == "TITLE":
        return None

    # Remove any surrounding quotes from the fields
    title = re.sub(r'^"|"$|^\'|\'$', r'', title)
    authors = re.sub(r'^"|"$|^\'|\'$', r'', authors)
    paths = re.sub(r'^"|"$|^\'|\'$', r'', paths)
    labels = re.sub(r'^"|"$|^\'|\'$', r'', labels)

    try:
        # Attempt to convert the authors field to a python list
        authors_list = ast.literal_eval(authors)
        # Attempt to convert the labels field to a python set
        labels_set = set(ast.literal_eval(labels))
        # Attempt to convert the paths field to a python list
        path_list = ast.literal_eval(paths)
        # Create the new TextData object
        obj = TextData(title, authors_list, path_list, labels_set)
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
