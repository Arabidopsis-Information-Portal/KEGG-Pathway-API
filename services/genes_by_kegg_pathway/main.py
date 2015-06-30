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
        id = args['pathway_id']

    org = 'map'
    if 'taxon_id' in args.keys():
        org = orgcode

    if not tools.valid_pathway_id(id):
        raise Exception('Not a valid identifier')
    id = org + id


    url = vars.url + 'get/' + id
    text = tools.openurl(url)
    data = tools.find_cat(text, 'gene')


    # Prints the data as a dict for Adama to return
    for element in data:
        print json.dumps(element)
        print '---'
