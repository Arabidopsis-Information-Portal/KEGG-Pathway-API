import requests
import json
import services.common.vars as vars
import services.common.tools as tools

def search(args):
    data = {}
    if 'identifier' in args.keys():
        url = vars.url + 'list/' + args['identifier']
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception("Can't access url" + url)
        text = r.text
        data = tools.two_col(text)
        
    else:
        url = vars.url + 'list/pathway/ath'
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception("Can't access url" + url)
        text = r.text
        data = tools.two_col(text)
               

        
    print json.dumps(data)
