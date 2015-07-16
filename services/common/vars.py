url = 'http://rest.kegg.jp/'
adama = 'https://api.araport.org/community/v0.3/'
find = 'find' # Searches databases for a given term
list = 'list' # Lists the entries in a database
get = 'get'   # Returns the given database entry and its associated data
delimiter = '\t'
fields = {"name", "description", "class", "module", "disease", "drug", \
"dblinks", "organism", "gene", "compound", "ko_pathway", "reference"}
