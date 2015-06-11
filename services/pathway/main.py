import requests
import json
import services.common.vars

def search(args):
    if 'identifier' in args.keys():
        url = vars.url + 'list/' + args['identifier']
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception("Can't access url")
        text = t.text;
    else:
        url = vars.url + list
