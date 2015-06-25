import json


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
                # Special case for REFERENCE
                if category == 'REFERENCE':
                    if 'REFERENCE' not in data.keys():
                        data['REFERENCE'] = []
                    reference = {}
                    reference['id'] = parts[1]
                    for i in range (0, 3):
                        split = text.split('\n', 1)
                        line = split[0];
                        text = split[1];
                        parts = line.split(None, 1)
                        reference[parts[0]] = parts[1]
                    data['REFERENCE'].append(reference)
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
        print category
        data2[category] = parse_cat(data[category], category)
    return data2

def parse_cat(data, field):
    field = field.upper()

    if field in {"NAME", "CLASS", "ORGANISM", "KO_PATHWAY", "DESCRIPTION"}:
        result = {field.lower(): data[0]}
        return result

    if field == 'GENE':
        arr = []
        for line in data:
            parts = line.split(None, 1)
            gene = {'locus':parts[0], field.lower():parts[1]}
            arr.append(gene)
        return arr

    if field in {"COMPOUND", "MODULE"}:
        arr = []
        for line in data:
            parts = line.split(None, 1)
            entry = {'id':parts[0], field.lower():parts[1]}
            arr.append(entry)
        return arr

    if field == "DBLINKS":
        arr = []
        for line in data:
            parts = line.split(None, 1)
            gene = {'database':parts[0][:-1], 'id':parts[1]}
            arr.append(gene)
        return arr
    return data
