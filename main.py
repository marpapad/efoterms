from pipeline import *
import argparse

parser = argparse.ArgumentParser(description="Efo Pipeline Arguments")
parser.add_argument("-hs", "--host", type=str, help="set postgres host, default: localhost", default='localhost')
parser.add_argument("-p", "--port", type=int, help="set postgres port, default: 5432", default=5432)
parser.add_argument("-db", "--db", type=str, help="set postgres database, default: efo", default='efo')
parser.add_argument("-u", "--user", type=str, help="set postgres user, default: postgres", default='postgres')
parser.add_argument("-P", "--password", type=str, help="set user password - required")
parser.add_argument("-pg", "--tillpage", type=int, help="set page upper limit - default 0", default=0)
args = parser.parse_args()

print(parser.print_help())

config = vars(args)
 
efoPipe(**config).run()

