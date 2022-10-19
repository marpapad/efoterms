from datetime import datetime
from pipeline.efo import *
import yaml

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

efodb = config['postgres']['db_efo']
api = config['api']['efo']

class efoPipe:
        
    """
    Incremental Efo Terms Pipe
    
    """
    
    def __init__(self,till_page):
        
        if (isinstance(till_page,int) or till_page is None) and till_page>0:
           raise ValueError('upper limit is not properly defined') 
        
        self.till_page = till_page
        
    def run(self):
        
        till_page = self.till_page
        size = api['size']
        
        try:
            lp = LastPage(efodb)
            # fetch last page
            pages_last_row = lp.fetch()
            
            if pages_last_row is not None and till_page < pages_last_row.page:
                raise ValueError('pages till given limit already load, try sth equal or greater than:' + str(pages_last_row.page))
            
            # if at least one page has been loaded in the past
            if pages_last_row is not None:
                last_page = pages_last_row.page
                last_page_elements = pages_last_row.elements
            # if no page has been loaded in the past
            else:
                last_page = -1 
                last_page_elements = 0
            # set starting point for incremental load
            if last_page<0:
                start_page = 0
                start_element = size * (-1)

            elif last_page>=0 and last_page_elements<size:
                start_page = last_page
                start_element = (size - last_page_elements) * (-1) 
                
            else:
                start_page = last_page + 1
                start_element = size * (-1)    

            #load each page and update the table pages with number of page and elements (terms) loaded
            for p in range(start_page,till_page+1):
                # starting point (element-wise)
                if p == start_page:
                    e = start_element 
                else:
                    e = size * (-1) 
                    
                # page retrieval
                efopg = efopage(**{**api,'page': p})
                page_elements = efopg.fetch()
                terms = page_elements['terms'][e:]
                # term and its attributes load & pages loaded update
                i = size + e
                for term in terms:
                    efo(efodb,term).insert()
                    if i == size + e and (pages_last_row is None or p!=last_page):
                        lp.insert(p,i+1)
                    else:
                        lp.update(p,{'elements':i+1,'createdat':datetime.now()})
                    i+=1
        except Exception as e:
             raise e
            

