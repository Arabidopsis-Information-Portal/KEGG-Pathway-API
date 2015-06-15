import requests
import json
import services.common.vars as vars
import services.common.tools as tools

def search(args):
    data = {}
    if 'identifier' in args.keys():
        if not tools.is_pathway(args['identifier']):
            raise Exception('Not a valid identifier')
        if 'field' in args.keys():
            url = vars.url + 'get/' + args['identifier']
            text = tools.openurl(url)
            arr = tools.find_cat(text, args['field'])

            if args['field'].upper() == "GENE":
                data = []
                for line in arr:
                    parts = line.split(None, 1)
                    gene = {'id':parts[0], 'name':parts[1]}
                    data.append(gene)
            else:
                data = arr
        else:
            url = vars.url + 'list/' + args['identifier']
            text = tools.openurl(url)
            data = tools.two_col(text, 'id', 'name')
        
    else:
        url = vars.url + 'list/pathway/ath'
        text = tools.openurl(url)
        data = tools.two_col(text, 'id', 'name')
               

        
    print json.dumps(data)
