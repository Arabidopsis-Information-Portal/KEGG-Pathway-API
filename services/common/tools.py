def two_col(text):
    data = {}
    lines = text.split('\n')
    for line in lines:     
        # splits each line into two parts by the tab delimiter with the
        # first part being the key and the second part being the value
        # in the returned JSON
        parts = line.split(vars.delimiter, 1);
        if len(parts) == 2:
            data[parts[0]] = parts[1]
    return data


def find_cat(text, cat):
    cat = cat.upper()
    lines = text.split('\n')
    flag = False;
    data = []
    for line in lines:
        parts = line.split(None, 1)
        if parts[0] == cat and not flag:
            data.append(parts[1])
            flag = True
        elif flag and line[0] != ' ':
            break
        elif flag:
            data.append(line.strip())
    return data
        
