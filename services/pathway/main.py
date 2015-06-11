import requests
import json
import services.common.vars as vars
import services.common.tools as tools

def search(args):
    data = {}
    if 'identifier' in args.keys():
        if 'field' in args.keys():
            url = vars.url + 'get/' + args['identifier']
            text = tools.openurl(url)
            data = tools.find_cat(text, args['field'])
        else:
            url = vars.url + 'list/' + args['identifier']
            text = tools.openurl(url)
            data = tools.two_col(text)
        
    else:
        url = vars.url + 'list/pathway/ath'
        text = tools.openurl(url)
        data = tools.two_col(text)
               

        
    print json.dumps(data)
