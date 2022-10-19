from efo import *
import yaml

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

efodb = config['postgres']['db_efo']
api = config['api']['efo']


# page = 1 

# efopg = efopage(**{**api,'page': page})

# page_elements = efopg.fetch()

# terms = page_elements['terms']

# i = 1
# for term in terms:
#     efo(efodb,term).insert()
#     i+=1
    
# page_elements = efopg.logit(efodb,i-1)


pages_last_row = LastPage(efodb).fetch()

if pages_last_row is not None:
    last_page = pages_last_row.page
    last_page_elements = pages_last_row.elements
else:
    last_page = -1 
    last_page_elements = 0
    
if last_page_elements<0:
   start_page = 0
   start_element = 0

elif last_page_elements>=0 and last_page_elements<api['size']:
   start_page = last_page
   start_element = api['size'] - last_page_elements -1
   
else:
   start_page = last_page + 1
   start_element = 0    

