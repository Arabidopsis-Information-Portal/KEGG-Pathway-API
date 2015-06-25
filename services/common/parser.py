import json
import services.common.vars as vars


def parse_ref(text):
    references = []
    split = text.split('\n', 1)
    line = split[0]
    while line != '':
        text = split[1]
        # ignores new lines and the /// that separates the results from the different queries
        if not (line == '' or line == '///'):
            # Special case for REFERENCE
            if category == 'reference':
                reference = {}
                reference['id'] = parts[1]
                for i in range (0, 3):
                    split = text.split('\n', 1)
                    line = split[0];
                    text = split[1];
                    parts = line.split(None, 1)
                    reference[parts[0].lower()] = parts[1]
                references.append(reference)
        split = text.split('\n', 1)
        line = split[0]

    return reference

def parse_fields(text):
    split = text.split('\n', 1)
    line = split[0]
    data = {}
    arr = []
    while line != '':
        text = split[1]
        # ignores new lines and the /// that separates the results from the different queries
        if not (line == '' or line == '///'):
            # If the line is defining a new category
            if line[0] != ' ':
                # splits the line into two parts by whitespace, with the first part being the category
                parts = line.split(None, 1)
                category = parts[0]
                category = category.lower()
                if category not in arr:
                    arr.append(category)
                if category == 'name':
                    data['name'] = parts[1]
                if category == 'entry':
                    data['identifier'] = parts[1].split()[0][3:]
        split = text.split('\n', 1)
        line = split[0]
    arr2 = []
    for field in arr:
        if field in vars.fields:
            arr2.append field

    data['fields'] = arr2
    return data;

def parse_cat(data, field):
    field = field.lower()

    if field in {"name", "class", "organism", "ko_pathway", "description"}:
        result = data[0]
        return field, result

    if field == 'gene':
        arr = []
        for line in data:
            parts = line.split(None, 1)
            gene = {'locus':parts[0], field.lower():parts[1]}
            arr.append(gene)
        return field, arr

    if field in {"compound", "module", "disease", "drug"}:
        arr = []
        for line in data:
            parts = line.split(None, 1)
            entry = {'id':parts[0], field.lower():parts[1]}
            arr.append(entry)
        return field, arr

    if field == "dblinks":
        arr = []
        for line in data:
            parts = line.split(None, 1)
            gene = {'database':parts[0][:-1], 'id':parts[1]}
            arr.append(gene)
        return field, arr
    return None, None

def parse_cat2(data, field):
    field = field.lower()

    if field in {"name", "class", "organism", "ko_pathway", "description"}:
        result = {field.lower(): data[0]}
        return result

    if field == 'gene':
        arr = []
        for line in data:
            parts = line.split(None, 1)
            gene = {'locus':parts[0], field.lower():parts[1]}
            arr.append(gene)
        return arr

    if field in {"compound", "module", "disease", "drug"}:
        arr = []
        for line in data:
            parts = line.split(None, 1)
            entry = {'id':parts[0], field.lower():parts[1]}
            arr.append(entry)
        return arr

    if field == "dblinks":
        arr = []
        for line in data:
            parts = line.split(None, 1)
            gene = {'database':parts[0][:-1], 'id':parts[1]}
            arr.append(gene)
        return arr
    return data
