import requests
import json
import services.common.vars as vars

def search(args):
    if 'identifier' in args.keys():
        url = vars.url + 'list/' + args['identifier']
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception("Can't access url" + url)
        text = r.text

    else:
        url = vars.url + 'list/pathway/ath'
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception("Can't access url" + url)
        text = r.text

        data = {}
        # Splits the received text into an array of lines
        lines = text.split('\n')
        for line in lines:     
            # splits each line into two parts by the tab delimiter with the
            # first part being the key and the second part being the value
            # in the returned JSON
            parts = line.split(vars.delimiter, 1);
            if len(parts) == 2:
                data[parts[0]] = parts[1]

        
    print json.dumps(data)
