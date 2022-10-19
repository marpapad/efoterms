from datetime import datetime
from pipeline.postgres import *
from pipeline.schema import *
import requests

class efopage:
    
    """
    Fetch Efo terms page through api &
    Log successfull inserts per page
    
    """
    
    def __init__(self,url,size,page):
        
        if not isinstance(size,int) or size<1 or size>500:
           raise ValueError('size not properly defined') 
        
        if not isinstance(page,int):
           raise ValueError('page number not properly defined') 
        
        self.page = page
        self.efopage = url + '?page={page}&size={size}'.format(page=page,size=size)
        
    def fetch(self):
        
        try:
        
            fetchpage = requests.get(self.efopage,timeout=3) 
            pagejson = fetchpage.json()
            response = {
            'terms' : pagejson['_embedded']['terms'],
            'pages' : pagejson['page']['totalPages']
            }
            
            return response
        
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
            
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
            
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
            
        except requests.exceptions.RequestException as err:
            print ("Error:",err)
            

class efo_db:
    
    """
    Efo schema 
    
    """

    def __init__(self,session):
        
        self.session = session
        
    def schema(self):

        tables = [
                    {
                        'table_obj' : Pages.__table__,
                        'table_name' : Pages.__tablename__,
                        'session' : self.session     
                    },                
                    {
                        'table_obj' : Term.__table__,
                        'table_name' : Term.__tablename__,
                        'session' : self.session     
                    },
                    {
                        'table_obj' : Description.__table__,
                        'table_name' : Description.__tablename__,
                        'session' : self.session     
                    },
                    {
                        'table_obj' : Synonym.__table__,
                        'table_name' : Synonym.__tablename__,
                        'session' : self.session     
                    },
                    {
                        'table_obj' : Ontology.__table__,
                        'table_name' : Ontology.__tablename__,
                        'session' : self.session    
                    },
                    {
                        'table_obj' : MeSH.__table__,
                        'table_name' : MeSH.__tablename__,
                        'session' : self.session     
                    }
                ]
        
        return tables
            

class efo:
    """
    Term & Attributes Mapping to Postgres
    
    """
    
    def __init__(self,psqlconfig,attributes):
        
        # check if input is dictionary
        if not isinstance(attributes,dict):
            raise ValueError("attributes should be a dictionary")
        
        # check if input is empty dictionary
        if not attributes:
            raise ValueError("attributes should not be empty")
        
        self.attributes = attributes
        
        self.psqlconfig = psqlconfig
        
    def term(self):
        """
        Efo term attibutes
        
        """
        # current timestamp
        ct = datetime.now()

        if self.attributes['label'] is None or self.attributes['label']=='':
            raise ValueError("term is missing")
        
        if self.attributes['iri'] is None or self.attributes['iri']=='':
            raise ValueError("iri is missing")
          
        term_attr = {
        
            'label' : self.attributes['label'],
            'iri' : self.attributes['iri'],
            'is_obsolete' : self.attributes['is_obsolete'] if 'is_obsolete' in self.attributes.keys() else False,
            'term_replaced_by' : self.attributes['term_replaced_by'] if 'term_replaced_by' in self.attributes.keys() else None,
            'is_defining_ontology' : self.attributes['is_defining_ontology'] if 'is_defining_ontology' in self.attributes.keys() else False,
            'has_children' : self.attributes['has_children'] if 'has_children' in self.attributes.keys() else False,
            'is_root' : self.attributes['is_root'] if 'is_root' in self.attributes.keys() else False,
            'is_preferred_root' : self.attributes['is_preferred_root'] if 'is_preferred_root' in self.attributes.keys() else False,
            'createdat' : ct
            }
        
        term_obj = Term(**term_attr)
        
        return term_obj
    
    def descriptions(self,term_obj):
        """
        Efo term descriptions
        
        """
        descriptions = self.attributes['description']
        
        if descriptions == []:
            
            descr_objs = []
        else:
            descr_objs = [Description(**{'description': descr,'term': term_obj}) for descr in descriptions]
            
        return descr_objs

    def synonyms(self,term_obj):
        """
        Efo term synonyms
        
        """
        synonyms = self.attributes['synonyms']
        
        if synonyms == []:
            
            synonym_objs = []
        else:
            synonym_objs = [Synonym(**{'synonym': synom,'term': term_obj}) for synom in synonyms]
            
        return synonym_objs

    def ontology(self,term_obj):
        """
        Efo term ontology
        
        """
        links = self.attributes['_links']
        
        if not 'parents' in links.keys():
            
            ontology_obj = None
            
        else :
            
            ontology = links['parents']['href']
            ontology_obj = Ontology(**{'ontology': ontology,'term': term_obj})
    
        return ontology_obj

    def mesh(self,term_obj):
        """
        Efo term MeSH xrefs
        
        """
        
        if not 'obo_xref' in self.attributes.keys():
            
            xrefs_objs = []
            
        else:
            
            xrefs = self.attributes['obo_xref']
            
            if xrefs is not None:
                
                xrefs_objs = [MeSH(**{**xref,'term': term_obj}) for xref in xrefs if xref['database']=='MeSH']
            else:
                
                xrefs_objs =[]
                
        return xrefs_objs
    
    def insert(self):
        """
        Insert efo elements
        
        """
        
        try: 
            
            psqlconfig = self.psqlconfig
            # create efo db if not exists
            PostgresConnector(psqlconfig).create_db()
            
            Session = PostgresConnector(psqlconfig).Session()
            
            # objects to insert per term
            term_obj = self.term()
            
            descr_objs = self.descriptions(term_obj)
            
            synomym_objs = self.synonyms(term_obj)
            
            ontology_obj = self.ontology(term_obj)
            
            mesh_objs = self.mesh(term_obj)
            
            with Session as s:
                
                schema = efo_db(s).schema()
                # create table if not exist
                for table in schema :
                    PostgresConnector(psqlconfig).create_table(**table)
                # insert objects within session
                s.add(term_obj)
                
                if descr_objs!=[]:
                    s.add_all(descr_objs)
                    
                if synomym_objs!=[]:
                    s.add_all(synomym_objs)
                    
                if ontology_obj is not None:  
                    s.add(ontology_obj)
                
                if mesh_objs!=[]:  
                    s.add_all(mesh_objs)
        
        except Exception as e:
            
            raise e 
        

class LastPage:
    """
    last page imported
    
    """
    
    def __init__(self,psqlconfig):
        
        self.psqlconfig = psqlconfig
        
    def fetch(self): 
           
        try: 
            
            psqlconfig = self.psqlconfig
            
            Session = PostgresConnector(psqlconfig).Session(expire_on_commit=False)
            
            with Session as s:
                
                last_page = PostgresConnector(psqlconfig).fetch_lastrow(Pages,'pages',s)
                
                return last_page
        
        except Exception as e:
            
            raise e 
    
    def update(self,page,new_attributes):
        
        try: 
            
            psqlconfig = self.psqlconfig
            
            Session = PostgresConnector(psqlconfig).Session(expire_on_commit=False)
            
            with Session as s:
                
                PostgresConnector(psqlconfig).updatebycol(Pages,'pages',s,'page',page,new_attributes)
        
        except Exception as e:
            
            raise e         
    
    def insert(self,page,elements):
        
        try :
            
            psqlconfig = self.psqlconfig
            
            page_attr = {
                'page' : page,
                'elements' : elements,
                'createdat' : datetime.now()
            }
            
            page_obj = Pages(**page_attr)
            
            Session = PostgresConnector(psqlconfig).Session()
            
            with Session as s:
                
                s.add(page_obj)

        except Exception as e:
            
            raise e 
        
        
        
        
        
        
    
        
        
    