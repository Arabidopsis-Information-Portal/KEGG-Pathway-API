import json
import requests
import services.common.vars as vars
import services.common.tools as tools
import re
from threading import Thread

# This is a function that will be used to convert Arth numbers into the standard
# AGI locus used on Araport. This function is used in the threading.
def convert_to_locus(element):
    url = vars.url + 'get/ath:' + element['locus_id']
    text = tools.openurl(url)
    links = tools.find_cat(text, 'dblinks')
    for dblink in links:
        if dblink['database'] == 'TAIR':
            element['locus_id'] = dblink['id']

# Adama-defined endpoint for doing a search. This endpoint will take a taxon ID
# and a pathway ID and return the genes in that pathway.
def search(args):
    # Checks if the required arguments are in the arguments received. If they
    # are not, raise an exception to tell the user.


    if 'pathway_id' not in args.keys():
        raise Exception('No argument given for "pathway_id"')



    if 'taxon_id' in args.keys():
        # Gets the required arguments
        taxon_id = args['taxon_id']
        path_id = args['pathway_id']


        # Uses the taxon ID to get the KEGG organism code and the name of the taxon
        orgcode, taxon_name = tools.taxon_to_kegg(taxon_id)
        # If the conversion was unsuccessful, raise an exception to notify the user
        if orgcode is None:
            raise Exception("Not a valid taxon id")

        # If the pathway_id is in an invalid format, raises an exception
        if not tools.valid_pathway_id(path_id):
            raise Exception('Not a valid identifier')

        # Creates the full pathway ID to access KEGG with
        path_id = orgcode + path_id




        # Gets the information from KEGG
        url = vars.url + 'get/' + path_id
        text = tools.openurl(url)



        # Parses the data received back, and creates an array that stores all teh genes.
        data = tools.find_cat(text, 'gene')

        # If the taxon specified is Arabidopsis, check if the returned genes are
        # valid
        if taxon_id == '3702':
            # Creates a regular expression to check if the locus IDs are valid
            p = re.compile('^AT[1-5CM]G[0-9]{5,5}$')

            # Creates a list that will store the threads that were created
            thread_list = []

            # Iterates through all the genes
            for element in data:
                # If the gene is not a valid locus ID
                if p.match(element['locus_id']) is None:
                    # Creates a new thread, starts it, and stores the thread in the
                    # list of threads.
                    thread = Thread(target = convert_to_locus, args = (element,))
                    thread.start()
                    thread_list.append(thread)

            # Joins with all threads so it will wait for all threads to finish
            for thread in thread_list:
                thread.join()


        raise Exception('here')

        # Prints the data as JSON for Adama to return
        for element in data:
            # Adds additional fields before printing.
            element['taxon_id'] = taxon_id
            element['taxon_name'] = taxon_name
            element['pathway_id'] = args['pathway_id']
            print json.dumps(element)
            print '---'

    else:
        path_id = args['pathway_id']

        # Gets the information from KEGG
        url = vars.url + 'get/ko' + path_id
        text = tools.openurl(url)



        # Parses the data received back, and creates an array that stores all the genes.
        data = tools.find_cat(text, 'orthology')

        for element in data:
            # Adds additional fields before printing.
            element['taxon_id'] = None
            element['taxon_name'] = None
            element['pathway_id'] = args['pathway_id']
            element['locus_id'] = None
            print json.dumps(element)
            print '---'

def list(args):

    # If a taxon_id is given
    if 'taxon_id' in args.keys():
        # Gets the taxon ID. For some unknown reason, the parameter received
        # from Adama is a list, so it must be accessed by getting the first
        # and only element of the list
        taxon_id = args['taxon_id'][0]
        # Uses the taxon ID to get the KEGG organism code and the name of the taxon
        orgcode, taxon_name = tools.taxon_to_kegg(taxon_id)
        # If the conversion was unsuccessful, raise an exception to notify the user
        if orgcode is None:
            raise Exception("Not a valid taxon id")

        # Accesses the KEGG API
        url = vars.url + 'list/pathway/' + orgcode
        text = tools.openurl(url)
        # Parses the text received into a list of pathways
        data = tools.two_col_path(text, taxon_id, taxon_name)

        # Prints the data in JSON form with elements in the list separated by
        # three dashes
        for element in data:
            print json.dumps(element)
            print '---'

    else:
        # Accesses the list of taxa from KEGG. Streaming is set to true because
        # KEGG streams the result, and since the data takes a couple seconds to
        # download, this will allow the adapter to start sending data to Adama
        # earlier so it can stream the data to the user.
        url = vars.url + "list/genome"
        r = requests.get(url, stream=True)

        # Iterates by line through the returned text
        for line in r.iter_lines():
            # Creates an empty dict to hold the taxon information
            org = {}
            # Parses the line to get the organism name and taxon ID
            parts1 = line.split('; ')
            parts = parts1[0].split(None, 3)
            if len(parts1) == 2 and len(parts) >= 3:
                org['taxon_id'] = parts[-1]
                org['taxon_name'] = parts1[-1]
                # Prints the data for Adama to send to the user
                print json.dumps(org)
                print '---'
