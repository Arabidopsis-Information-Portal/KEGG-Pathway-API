import requests
import json
import services.common.vars as vars
import services.common.tools as tools

def search(args):
    data = {}
    # If a specific pathway is given
    if 'identifier' in args.keys():
        # If the pathway given is nto actually a pathway, raise an exception
        if not tools.is_pathway(args['identifier']):
            raise Exception('Not a valid identifier')
        # If a field of the specific pathway is requested
        if 'field' in args.keys():
            url = vars.url + 'get/' + args['identifier']
            text = tools.openurl(url)
            arr = tools.find_cat(text, args['field'])

#            if args['field'].upper() == "GENE":
#                data = []
#                for line in arr:
#                    parts = line.split(None, 1)
#                    gene = {'id':parts[0], 'name':parts[1]}
#                    data.append(gene)
#            else:
            data = arr
        # No field is specified
        else:
            url = vars.url + 'list/' + args['identifier']
            text = tools.openurl(url)
            data = tools.two_col(text, 'id', 'name')
    # No pathway is specifie. Lists all pathways in Arabidopsis
    else:
        url = vars.url + 'list/pathway/ath'
        text = tools.openurl(url)
        data = tools.two_col(text, 'id', 'name')
               

    print json.dumps(data)
