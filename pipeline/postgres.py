from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.schema import CreateTable
from sqlalchemy.exc import OperationalError
from sqlalchemy import inspect
from contextlib import contextmanager
from sqlalchemy import update

class ValidationError(Exception):
    def __init__(self, msg):
        self.msg = msg

class PostgresURI(object):
    
    def __init__(self,params):
        
        # check if input is dictionary
        if not isinstance(params,dict):
            raise ValueError("params should be a dictionary")
        
        # check if input is empty dictionary
        if not params:
            raise ValueError("params should not be empty")
        
        # check if host is defined
        if ('host' not in params) or (not isinstance(params['host'],str)) or (params['host']==''):
           raise ValidationError('host is missing or not properly defined')

        # check if user is defined
        if ('user' not in params) or (not isinstance(params['user'],str)) or (params['user']==''):
           raise ValidationError('username is missing or not properly defined')   
       
        # check if password is defined
        if ('password' not in params) or (not isinstance(params['password'],str)) or (params['password']==''):
           raise ValidationError('password is missing or not properly defined') 
        
        # check if db is defined
        if ('db' not in params) or (not isinstance(params['db'],str)) or (params['db']==''):
           raise ValidationError('db is missing or not properly defined') 
        
        # check if port is defined
        if ('port' not in params) or (not isinstance(params['port'],int)):
           raise ValidationError('port is missing or not properly defined')   
        
        self.params = params
    
    def __str__(self) -> str:
        postgres_uri = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'.format(**self.params)
        return postgres_uri
    
class PostgresConnector(PostgresURI):
        
    def __init__(self,*args,**kwargs):
        super(PostgresConnector,self).__init__(*args,**kwargs)
        
    def uri(self) -> str:
        return super(PostgresConnector,self).__str__()
    
    def engine(self):
        uri = self.uri()
        return create_engine(uri)
    
    def create_db(self):
        try:
            engine = self.engine()
            if not database_exists(engine.url):
                create_database(engine.url)
                               
        except OperationalError as exc:
            raise exc
    
    def teble_exists(self,name):
        engine = self.engine()
        return True if inspect(engine).has_table(name) else False
    
    @contextmanager
    def Session(self,*args, **kwargs):
        Session = scoped_session(sessionmaker(bind=self.engine(),*args, **kwargs))
        session = Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.expunge_all()
            session.close()
    
    def create_table(self,table_obj,table_name,session):
        try:
            if not self.teble_exists(table_name):
                session.execute(CreateTable(table_obj))
        except OperationalError as exc:
            raise exc
    
    def fetch_lastrow(self,table_obj,table_name,session):
        engine = self.engine()
        if database_exists(engine.url) and self.teble_exists(table_name):
            obj = session.query(table_obj).order_by(table_obj.id.desc()).first()
        else:
            obj = None
        return obj
    
    # filter by single column and update attributes dynamically
    def updatebycol(self,table_obj,table_name,session,attr,value,new_attibutes):
        try:
            
            engine = self.engine()
            if database_exists(engine.url) and self.teble_exists(table_name):
                stmt = (
                    update(table_obj).
                    where(getattr(table_obj,attr)==value).
                    values(new_attibutes)
                    
                )
                session.execute(stmt)
                
        except Exception as exc:
            raise exc


        
    
    
          
        
    
    

