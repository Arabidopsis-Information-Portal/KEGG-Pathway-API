import requests
import json
import services.common.vars as vars
import services.common.tools as tools
import services.common.parser as parser

def search(args):
    data = {}
    # Converting the given taxon id into the KEGG organism code
    tid = ''
    orgcode = ''
    if 'taxon_id' in args.keys():
        tid = args['taxon_id']
        orgcode = tools.taxon_to_kegg(tid)
        if orgcode is None:
            raise Exception("Not a valid taxon id")

    # If a pathway id is specified
    if 'pathway_id' in args.keys():
        # Sets the default organism code to map
        org = 'map'
        if 'taxon_id' in args.keys():
            org = orgcode
        # If the pathway given is not in the form of a KEGG pathway id, raises
        # exception.
        if not tools.valid_pathway_id(args['pathway_id']):
            raise Exception('Not a valid identifier')
        id = org + args['pathway_id']

        url = vars.url + 'get/' + id
        text = tools.openurl(url)
        data = parser.parse(text)

        print json.dumps(data)
        return

    else: #No pathway specified
        org = ''
        if 'taxon_id' in args.keys():
                org = orgcode

        url = vars.url + 'list/pathway/' + org
        text = tools.openurl(url)
        data = tools.two_col_path(text, orgcode)

    # Prints the data as a dict for Adama to return
    for element in data:
        print json.dumps(element)
        print '---'
