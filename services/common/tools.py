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
            element['taxon_id'] = org
            element['KEGG_pathway_id'] = parts[0][8:]
            element['KEGG_pathway_name'] = parts[1]
            data.append(element)
    return data


# Splits the human readable text from the KEGG get operations. Finds the
# category and calls a parser to convert the lines into a more useable JSON
def find_cat(text, cat):
    cat = cat.upper()
    if cat not in vars.fields:
        raise Exception("Not a valid field")
    lines = text.split('\n')
    flag = False;
    data = []
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
    return parser.parse(data, cat)

# Opens a given url and returns the text. It will throw an exception if it
# receives a non 200 status code
def openurl(url):
    import datetime
    today = datetime.date.today()
    parts = url.split('/')
    file_name = parts[-3] + '_' + parts[-2] + '_' + parts[-1] + '.txt'
    try:
        file = open(file_name, 'r')
        s = file.readline()[:-1]
        if s != str(today):
            file.close()
            raise Exception()
    except Exception:
        file = open(file_name, 'w')
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception("Can't access url " + url)
        file.write(str(today) +'\n')
        file.write(r.text)
        file.close()
        return r.text

    return file.read();



# Checks if the pathway ID given is 5 digits
def valid_pathway_id(id):
    p = re.compile('[0-9]{5}$')
    if p.match(id) is None:
        return False
    return True


# Checks online for if the given ID is in the list of pathways for Arabidopsis
# Not used anymore
def is_pathway(id):
    text = openurl(vars.url+"list/pathway/ath")
    lines = text.split('\n')
    for line in lines:
        parts = line.split(vars.delimiter, 1);
        if parts[0][5:] == id:
            return True
    return False

# Checks the KEGG API to convert an NCBI taxon ID into a KEGG organism code
def taxon_to_kegg(id):

    genome_list = open('services/common/genomes.txt', 'r');
    text = genome_list.read();
    lines = text.split('\n')
    for line in lines:
        parts1 = line.split(';')
        parts = parts1[0].split(None, 3);
        if len(parts1) == 2 and len(parts) >= 3:
            if parts[-1] == id:
                return parts[1][:-1]
    return None
