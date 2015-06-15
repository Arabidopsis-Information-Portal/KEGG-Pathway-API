import json

def parse(data, field):
    field = field.upper()

    if field in {"NAME", "CLASS", "ORGANISM", "KO_PATHWAY", "DESCRIPTION"}:
        result = {field.lower(): data[0]}
        return result

    if field in {"GENE", "COMPOUND", "MODULE", "DISEASE", "DRUG"}:
        arr = []
        for line in data:
            parts = line.split(None, 1)
            gene = {'id':parts[0], field.lower():parts[1]}
            arr.append(gene)
        return arr

    if field == "DBLINKS":
        arr = []
        for line in data:
            parts = line.split(None, 1)
            gene = {'database':parts[0][:-1], 'id':parts[1]}
            arr.append(gene)
        return arr
    return data
