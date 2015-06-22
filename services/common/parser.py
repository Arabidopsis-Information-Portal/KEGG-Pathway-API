import json

def parse(data, field):
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
