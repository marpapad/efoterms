from datetime import datetime
from pipeline.efo import *
import yaml
import requests

with open('pipeline/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

api = config['api']['efo']

class efoPage:
    
    """
    Fetch Efo terms page through api &
    Log successfull inserts per page
    
    """
    
    def __init__(self,page):
        
        if not isinstance(api['size'],int) or api['size']<1 or api['size']>500:
           raise ValueError('size not properly defined') 
        
        if not isinstance(page,int):
           raise ValueError('page number not properly defined') 
        
        self.page = page
        self.efopage = api['url'] + '?page={page}&size={size}'.format(page=page,size=api['size'])
        
    def fetch(self):
        
        try:
        
            fetchpage = requests.get(self.efopage,timeout=3) 
            pagejson = fetchpage.json()
            if '_embedded' in pagejson.keys():
                
                response = {
                'terms' : pagejson['_embedded']['terms'],
                'pages' : pagejson['page']['totalPages']
                }
                return response
            else:
                print('Not available page')   
            
        
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
            
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
            
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
            
        except requests.exceptions.RequestException as err:
            print ("Error:",err)
            


class efoPipe:
        
    """
    Incremental Efo Terms Pipe
    
    """
    
    def __init__(self,till_page,user,password,host,port,db):
        
        if not(isinstance(till_page,int) or till_page is None) or till_page<0:
           raise ValueError('upper limit is not properly defined') 
        
        self.till_page = till_page
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db = db
        
    def run(self):
        
        till_page = self.till_page
        size = api['size']
        
        efodb = {
                 'host': self.host,
                 'user': self.user,
                 'password': self.password,
                 'port': self.port,
                 'db': self.db 
                 }
 
        try:
            lp = LastPage(efodb)
            # fetch last page
            pages_last_row = lp.fetch()
            
            # if pages_last_row is not None :
            #     print('start page: ',pages_last_row.page)
            # else:
            #     print('no page has been loaded yet')
            
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
                efopg = efoPage(p)
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
            

