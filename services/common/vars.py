url = 'http://rest.kegg.jp/'
find = 'find' # Searches databases for a given term
list = 'list' # Lists the entries in a database
link = 'link' # Finds related entries in other databases
conv = 'conv' # Converts between KEDD identifiers and outside identifiers
info = 'info' # Gets information about the given database
get = 'get'   # Returns the given database entry and its associated data
delimiter = '\t'
fields = {"NAME", "DESCRIPTION", "CLASS", "MODULE", "DISEASE", "DRUG", \
"DBLINKS", "ORGANISM", "GENE", "COMPOUND", "KO_PATHWAY", "REFERENCE"}
