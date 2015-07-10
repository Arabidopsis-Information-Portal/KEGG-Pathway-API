import services.common.vars as vars
import services.common.parser as parser
import requests
import re

# Splits text first by line, and then by the deliminator from the vars file.
# text is the text to be parsed into a JSON, and str1 and str2 are the keys that
# will map to the values of the two columns
def two_col(text, str1, str2):
    data = []
    lines = text.split('\n')
    for line in lines:
        # splits each line into two parts by the tab delimiter with the
        # first part being the key and the second part being the value
        # in the returned JSON
        parts = line.split(vars.delimiter, 1);
        if len(parts) == 2:
            element = {}
            element[str1] = parts[0]
            element[str2] = parts[1]
            data.append(element)
    return data

# Parses text like two_col but uses set keys and also adds a key-value pair for
# the taxon_id. If no ID is provided (empty string), then taxon_id will be set
# to null
def two_col_path(text, org):
    if org == '':
        org = None
    data = []
    lines = text.split('\n')
    for line in lines:
        # splits each line into two parts by the tab delimiter with the
        # first part being the key and the second part being the value
        # in the returned JSON
        parts = line.split(vars.delimiter, 1);
        if len(parts) == 2:
            element = {}
            #element['organism'] = org
            element['identifier'] = parts[0][8:]
            if org is None:
                element['name'] = parts[1]
            else:
                element['name'] = parts[1].rsplit(' - ', 1)[0]
            data.append(element)
    return data


# Splits the human readable text from the KEGG get operations. Finds the
# category and calls a parser to convert the lines into a more useable JSON
def find_cat(text, cat):
    cat = cat.lower()
    if cat not in vars.fields:
        raise Exception("Not a valid field")
    if cat == "reference":
        return parser.parse_ref(text)
    lines = text.split('\n')
    flag = False;
    data = []
    cat = cat.upper()
    for line in lines:
        parts = line.split(None, 1)
        if len(parts) == 0:
            return {}
        if parts[0] == cat and not flag:
            data.append(parts[1])
            flag = True
        elif flag and line[0] != ' ':
            break
        elif flag:
            data.append(line.strip())
    cat = cat.lower()
    return parser.parse_cat2(data, cat)

# Opens a given url and returns the text. It will throw an exception if it
# receives a non 200 status code
def openurl(url):
    r = requests.get(url)
    if r.status_code == 404:
        raise Exception("Not Found: Can't access url " + url)
    elif r.status_code != 200:
        raise Exception("Can't access url " + url)
    return r.text

# Checks if the pathway ID given is 5 digits
def valid_pathway_id(id):
    p = re.compile('[0-9]{5}$')
    if p.match(id) is None:
        return False
    return True

# Checks the KEGG API to convert an NCBI taxon ID into a KEGG organism code
def taxon_to_kegg(id):
    url = vars.url+"find/genome/" + id
    text = openurl(url)

    lines = text.split('\n')
    for line in lines:
        parts1 = line.split(';')
        parts = parts1[0].split(None, 3);
        if len(parts1) == 2 and len(parts) >= 3:
            if parts[-1] == id:
                return parts[1][:-1]
    return None
