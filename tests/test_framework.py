import requests

token = '8ee64b64a914208e11415a6276b9e71a'
url = "https://api.araport.org/community/v0.3/bliu/pathway_v0.1"
keggurl = "http://rest.kegg.jp"





def test1():
    header = {'Authorization': 'Bearer ' + token}
    r = requests.get(url + '/search', headers = header)
    response = r.json()
    data = response['result'][0]
    string = ''
    for pathway in data:
        string += pathway['id'] + '\t' + pathway['name']+'\n'
        
    r2 = requests.get(keggurl + '/list/pathway/ath')
    string2 = r2.text
    print string ==  string2


test1()
