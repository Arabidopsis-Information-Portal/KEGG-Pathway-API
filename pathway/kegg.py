import urllib2
import json
import vars
import requests


def search(args):
    # Checks the provided int for the required arguments 'operation' and 
    # 'argument'
    if not 'operation' in args.keys():
        exit(1);
    if not 'argument' in args.keys():
        exit(1);

    # Builds the url
    url = vars.url
    operation = args['operation']
    argument = args['argument']
    url+= operation + '/' + argument

    # adds the optional arguments if they exist

    if 'argument2' in args.keys() and args['argument2'] != 'None':
        url+= '/' + args['argument2']
    if 'option' in args.keys() and args['option'] != 'None':
        url+= '/' + args['option']

    r = requests.get(url);
    text = r.text;

    # Gets the text from the url
    try:
        response = urllib2.urlopen(url)
        text = response.read()
    except Exception:
        raise ValueError("Bad URL: " + url)
    data = {}

    # This part handles the find, list, link, and conv operations as
    # detailed by the KEGG API. 
    if operation == vars.find or operation == vars.list\
            or operation == vars.link or operation == vars.conv:
        # Splits the received text into an array of lines
        lines = text.split('\n')
        for line in lines:     
            # splits each line into two parts by the tab delimiter with the
            # first part being the key and the second part being the value
            # in the returned JSON
            parts = line.split(vars.delimiter, 1);
            if len(parts) == 2:
                data[parts[0]] = parts[1]

    # Parses results from the get operation
    elif operation == vars.get:
        # splits the text into lines
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


    
    # Prints the JSON to standard out for ADAMA to convert into a JSON to 
    # return.
    print json.dumps(data);
