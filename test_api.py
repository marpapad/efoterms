from pipeline import *

till_page = 15
host = 'localhost'
db = 'efo'
user = 'postgres'
password = 'intell1Pass'
port = 5432
 
parameters = {
    'till_page' :till_page,
    'host': host,
    'user': user,
    'password': password,
    'port': port,
    'db': db             
    }

efoPipe(**parameters).run()

