import services.common.vars as vars


def extract_ids(string):
    data = {}
    parts = string.split(' [', 1)
    id_string = parts[1][:-1]
    while id_string[:3] != 'KO:' and id_string[:3] != 'EC:':
        id_string = id_string.split(' [', 1)[1]
    ids = id_string.split('] [')
    print ids
    for a in ids:
        if 'EC:' == a[:3] and 'ec' not in data:
            data['ec'] = a[3:]
        elif 'KO:' == a[:3] and 'ko' not in data:
            data['ko'] = a[3:]
    return parts[0], data

def parse(text):
    data = {}
    split = text.split('\n', 1)
    line = split[0]
    while line != '':
        text = split[1]
        # ignores new lines and the /// that separates the results from the different queries
        if not (line == '' or line == '///'):
            # If the line is not defining a new category, adds the line to the existing category
            if line[0] == ' ':
                data[category].append(line.strip()) # removes leading and trailing whitespace
            else:    # If the line is defining a new category
                # splits the line into two parts by whitespace, with the first part being the category
                parts = line.split(None, 1)
                category = parts[0]
                category = category.lower()
                # Special case for REFERENCE
                if category == 'reference':
                    if 'reference' not in data.keys():
                        data['reference'] = []
                    reference = {}
                    if len(parts) == 1:
                        reference['id'] = None
                    else:
                        reference['id'] = parts[1]
                    for i in range (0, 3):
                        split = text.split('\n', 1)
                        line = split[0]
                        text = split[1]
                        parts = line.split(None, 1)
                        if len(parts) != 1:
                            reference[parts[0].lower()] = parts[1]
                        else:
                            reference[parts[0].lower()] = ''
                    data['reference'].append(reference)
                else:
                    # Creates a new array to hold lines under that category
                    data[category] = []
                    # Second part is the rest of the line, going under the category
                    if len(parts) > 1:
                        data[category].append(parts[1])
        split = text.split('\n', 1)
        line = split[0]
    data2 = {}
    for category in data:
        key, value = parse_cat(data[category], category)
        if key is not None:
            data2[key] = value
    return data2

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
            arr2.append(field)

    data['fields'] = arr2
    return data

def parse_cat(data, field):
    field = field.lower()

    if field in {"name", "class", "organism", "ko_pathway", "description"}:
        result = data[0]
        return field, result

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
            name, ids = extract_ids(parts[1])
            gene = {'locus_id':parts[0], 'gene_name':name}
            if 'ec' in ids:
                gene['ec_number'] = ids['ec']
            if 'ko' in ids:
                gene['kegg_orthology_id'] = ids['ko']
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
