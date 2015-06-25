import requests
import json
import services.common.vars as vars
import services.common.tools as tools
import services.common.parser as parser
from threading import Thread

# Used for threading when searching pathways of an organism
def pathway_set(org, return_data):
    url = vars.url + 'list/pathway/' + org
    text = tools.openurl(url)
    data = set()
    lines = text.split('\n')

    # Creates a set of the ids of the pathways in the given organism
    for line in lines:
        parts = line.split(vars.delimiter, 1);
        if len(parts) == 2:
            data.add(parts[0][8:])
    return_data.append(data);


def search(args):
    data = {}
    # Converting the given taxon id into the KEGG organism code
    tid = ''
    if 'taxon_id' in args.keys():
        tid = args['taxon_id']
        orgcode = tools.taxon_to_kegg(tid)
        if orgcode is None:
            raise Exception("Not a valid taxon id")

    # If a pathway id is specified
    if 'identifier' in args.keys():
        # Sets the default organism code to map
        org = 'map'
        if 'taxon_id' in args.keys():
            org = orgcode
        # If the pathway given is not in the form of a KEGG pathway id, raises
        # exception.
        if not tools.valid_pathway_id(args['identifier']):
            raise Exception('Not a valid identifier')
        id = org + args['identifier']

        # If a field of the specific pathway is requested.
        if 'field' in args.keys() and args['field'] != 'none':
            url = vars.url + 'get/' + id
            text = tools.openurl(url)
            data = tools.find_cat(text, args['field'])

            # Special case for returning JSON when a field is specified


        # No field is specified
        else:
            url = vars.url + 'get/' + id
            text = tools.openurl(url)
            data = parser.parse_fields(text)

        print json.dumps(data)
        return

    # If the user has provided a search term to search pathways for
    elif 'term' in args.keys():
        term = args['term']

        # If no species is provided, just gets from the KEGG find function
        if 'taxon_id' not in args.keys():
            url = vars.url + 'find/pathway/' + term
            text = tools.openurl(url)
            data = tools.two_col_path(text, '')

        # If a species is specified, has to confirm that the pathway exists in
        # the given species
        else:
            org = orgcode
            return_data = []

            thread = Thread(target = pathway_set, args = (org, return_data))
            thread.start()
            # First searches all pathways
            url = vars.url + 'find/pathway/' + term
            text = tools.openurl(url)
            tempdata = tools.two_col_path(text, tid)
            # Then lists all pathway in given organism

            thread.join()
            data2 = return_data[0]

            data = []

            # Takes the intersection of both lists
            for element in tempdata:
                if element['KEGG_pathway_id'] in data2:
                    data.append(element)

    # No pathway is specified. Lists all pathways in Arabidopsis
    else:
        org = ''
        if 'taxon_id' in args.keys():
                org = orgcode

        url = vars.url + 'list/pathway/' + org
        text = tools.openurl(url)
        data = tools.two_col_path(text, tid)

    # Prints the data as a dict for Adama to return
    for element in data:
        print json.dumps(element)
        print '---'
