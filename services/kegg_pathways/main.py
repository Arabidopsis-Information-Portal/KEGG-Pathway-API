import requests
import json
import services.common.vars as vars
import services.common.tools as tools
import services.common.parser as parser

def search(args):
    data = {}
    # Converting the given taxon id into the KEGG organism code
    orgcode = ''
    if 'taxon_id' in args.keys():
        orgcode = tools.taxon_to_kegg(args['taxon_id'])
        if orgcode is None:
            raise Exception("Not a valid taxon id")

    # If a pathway id is specified, it will get fields of the specific pathway
    if 'pathway_id' in args.keys():
        # Sets the default organism code to map if no organism is specified
        org = 'map'
        if 'taxon_id' in args.keys():
            org = orgcode
        # If the pathway given is not in the form of a KEGG pathway id, raises
        # exception.
        if not tools.valid_pathway_id(args['pathway_id']):
            raise Exception('Not a valid pathway ID')

        # Creates the full KEGG pathway ID with organism code and pathway ID
        id = org + args['pathway_id']

        # Accesses the KEGG API
        url = vars.url + 'get/' + id
        text = tools.openurl(url)

        # Parses the text received from the KEGG API
        data = parser.parse(text)

        # Adds the pathway ID to the returned information
        data['pathway_id'] = args['pathway_id']

        # Removes the organism name from the pathway
        if org != '' and 'name' in data:
            data['name'] = data['name'].rsplit(' - ', 1)[0]

        # Prints the data for ADAMA to return to the user
        print json.dumps(data)

    else: #No pathway specified

        # If an organism is given, set it to search through that organism
        org = ''
        if 'taxon_id' in args.keys():
                org = orgcode

        # Accesses the KEGG API
        url = vars.url + 'list/pathway/' + org
        text = tools.openurl(url)

        # Parses the text received into a list of pathways
        data = tools.two_col_path(text, orgcode)

        # Prints the data in JSON form with elements in the list separated by
        # three dashes
        for element in data:
            print json.dumps(element)
            print '---'

def list(args):
    raise Exception('Not implemented yet')
