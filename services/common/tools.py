import services.common.vars as vars
import services.common.parser as parser
import requests
import re

# Splits text first by line, and then by 
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
            element['organism'] = org
            element['KEGG_pathway_id'] = parts[0][8:]
            element['KEGG_pathway_name'] = parts[1]
            data.append(element)
    return data





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

def openurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("Can't access url " + url)
    return r.text

def valid_pathway_id(id):
    p = re.compile('[0-9]{5}$')
    if p.match(id) is None:
        return False
    return True



def is_pathway(id):
    text = openurl(vars.url+"list/pathway/ath")
    lines = text.split('\n')
    for line in lines:
        parts = line.split(vars.delimiter, 1);
        if parts[0][5:] == id:
            return True
    return False
