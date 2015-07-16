import json
import requests
import services.common.vars as vars
import services.common.tools as tools


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

def list(args):
    name = 'genes_by_kegg_pathway'
    version = '0.2'

    try:
        f = open('metadata.yml', 'r')
        flag1 = False
        flag2 = False
        for line in f:
            if line[:5] == 'name:':
                name = line.split(None, 1)[1]
                flag1 = True
            elif line[:5] == 'version:':
                version = line.split(None, 1)[1]
                flag2 = True
            if flag1 and flag2:
                break

    except IOError:
        name = 'genes_by_kegg_pathway'
        version = '0.2'


    if 'taxon_id' in args.keys():
        taxon_id = args['taxon_id']
        raise Exception(taxon_id)
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
            #element['url'] = vars.adama + 'bliu-dev/' + name + '_v' + version + '/search?taxon_id=' + taxon_id + '&pathway_id=' + element['pathway_id']
            print element['pathway_id']
            #print json.dumps(element)
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
                org['url'] = vars.adama + 'bliu-dev/' + name + '_v' + version + '/list?taxon_id=' + parts[-1]
                org['taxon_name'] = parts1[-1]
                print json.dumps(org)
                print '---'
