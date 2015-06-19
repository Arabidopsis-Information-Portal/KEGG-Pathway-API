import services.pathway.main as m
import requests
import time
import sys
import os
import warnings



def run(token, args):
    warnings.simplefilter("ignore")
    for i in range(1, 10):
#        sys.stdout = open(os.devnull, "w")
        sec = time.time()
        m.search(args);
        sec = time.time() - sec
        url = 'https://api.araport.org/community/v0.3/bliu/pathway_v0.1/search'
        headers = {'Authorization':'Bearer ' + token}
        sec2 = time.time()
        r = requests.get(url, headers = headers, params=args)
        sec2 = time.time() - sec2
        sys.stdout = sys.__stdout__
        print sec, sec2, sec2 - sec
