import urllib2
import json

#response = urllib2.urlopen('http://rest.kegg.jp/list/pathway/ath')
#html = response.read()
#lines = html.split('\n');
#data = {};

#for line in lines:
#    parts = line.split('\t');
#    if len(parts) >= 2:
#        data[parts[0]] = parts[1]

#json_data = json.dumps(data)
#print json_data

def search(args):
    if not 'operation' in args.keys():
        exit(1);
    if not 'argument' in args.keys():
        exit(1);

    url = 'http://rest.kegg.jp/'
    operation = args['operation']
    argument = args['argument']
    url+= operation + '/' + argument

    if 'argument2' in args.keys():
        url+= '/' + args['argument2']
    
    if 'option' in args.keys():
        url+= '/' + args['option']
    
    response = urllib2.urlopen(url)
    html = response.read()
    data = {}

    if operation == 'find' or operation == 'list'\
            or operation == 'link' or operation == 'conv':
        print "jsonizing"
        lines = html.split('\n')
        for line in lines:     
            parts = line.split('\t');
            if len(parts) >= 2:
                data[parts[0]] = parts[1]
    

    result = {}
    result['results'] = data
    result['args'] = args

    print json.dumps(result);
