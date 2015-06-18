import requests
import json
import services.common.vars as vars
import services.common.tools as tools
import time
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
    # Way to send data back to parent
    return_data.append(data);



def search(args):
    sec = time.time();
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

        # If a field of the specific pathway is requested. Can still be used,
        # but is not displayed in any documentation.
        if 'field' in args.keys():
            url = vars.url + 'get/' + id
            text = tools.openurl(url)
            data = tools.find_cat(text, args['field'])

        # No field is specified
        else:
            url = vars.url + 'list/' + id
            text = tools.openurl(url)
            data = tools.two_col_path(text, tid)

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

            # Creates a new thread to get all the pathways in an an organism
            thread = Thread(target = pathway_set, args = (org, return_data))
            thread.start()

            # Do a search on all pathways
            url = vars.url + 'find/pathway/' + term
            text = tools.openurl(url)
            tempdata = tools.two_col_path(text, tid)

            # waits until both parts finish
            thread.join()
            # gets the data from the thread
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

    print time.time()-sec
    # Prints the data as a dict for Adama to return
    #print json.dumps(data)
