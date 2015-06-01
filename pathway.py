import json
import urllib2

def search(args):
    if not 'gene' in args.keys():
        exit(1)
    
    gene = args['gene']
    url = 'http://rest.kegg.jp/'
    response = urllib2.urlopen(url+'/get/ath:'+gene)
    html = response.read()
    lines = html.split('\n')
    flag = False
    data = {}
    for line in lines:
        if line[:7] == "PATHWAY" and not flag:
            words = line.split(None, 2);
            data[words[1]] = words[2]
            flag = True
        elif flag and line[0] != ' ':
            break
        elif flag:
            words = line.split(None, 1);
            data[words[0]] = words[1]
    
    results = {}
    results['pathways'] = data;
    results['gene'] = gene;
    print json.dumps(results);
