import urllib2
import json
import vars



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

    if 'argument2' in args.keys():
        url+= '/' + args['argument2']
    if 'option' in args.keys():
        url+= '/' + args['option']
    
    # Gets the text from the url
    response = urllib2.urlopen(url)
    text = response.read()
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
        lines = text.split('\n')
        
        for line in lines:
            # ignores new lines and the /// that separates the results from the different queries
            if line == '' or line == '///':
                continue
            # If the line is not defining a new category
            if line[0] == ' ':
                # Adds the line to the existing category after removing leading and trailing whitespace
                data[category].append(line.strip())
            # If the line is defining a new category
            else:
                # splits the line into two parts by whitespace
                parts = line.split(None, 1)
                # first part is the name of the category
                category = parts[0]
                # creates a new array of lines under that category
                data[category] = []
                # Second part is the rest of the line, going under the category
                if len(parts) > 1:
                    data[category].append(parts[1])


    
    # Prints the JSON to standard out for ADAMA to convert into a JSON to 
    # return.
    print json.dumps(data);
