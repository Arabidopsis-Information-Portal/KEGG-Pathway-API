import json
import requests
import services.common.vars as vars
import services.common.tools as tools


def search(args):
    data = {}
    # Converting the given taxon id into the KEGG organism code
    taxon_id = ''
    orgcode = ''
    if 'taxon_id' in args.keys():
        taxon_id = args['taxon_id']
        orgcode, taxon_name = tools.taxon_to_kegg(taxon_id)
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
        element['taxon_id'] = taxon_id
        element['taxon_name'] = taxon_name
        element['pathway_id'] = args['pathway_id']
        print json.dumps(element)
        print '---'

def list(args):

    if 'taxon_id' in args.keys():
        taxon_id = args['taxon_id'][0]
        orgcode, taxon_name = tools.taxon_to_kegg(taxon_id)
        if orgcode is None:
            raise Exception("Not a valid taxon id")
        org = ''
        if 'taxon_id' in args.keys():
            org = orgcode


        # Accesses the KEGG API
        url = vars.url + 'list/pathway/' + org
        text = tools.openurl(url)
        # Parses the text received into a list of pathways
        data = tools.two_col_path(text, taxon_id, taxon_name)

        # Prints the data in JSON form with elements in the list separated by
        # three dashes
        for element in data:
            print json.dumps(element)
            print '---'

    else:
        url = vars.url + "list/genome"
        r = requests.get(url, stream=True)

        for line in r.iter_lines():
            org = {}
            parts1 = line.split('; ')
            parts = parts1[0].split(None, 3)
            if len(parts1) == 2 and len(parts) >= 3:
                org['taxon_id'] = parts[-1]
                org['taxon_name'] = parts1[-1]
                print json.dumps(org)
                print '---'
