from pipeline import *
import argparse


if __name__ == '__main__':

    fp = efoPage(0).fetch()
    total_pages = fp['pages']

    parser = argparse.ArgumentParser(description="Efo Pipeline Arguments")
    parser.add_argument("-hs", "--host", type=str, help="set postgres host, default: localhost", default='localhost')
    parser.add_argument("-p", "--port", type=int, help="set postgres port, default: 5432", default=5432)
    parser.add_argument("-db", "--db", type=str, help="set postgres database, default: efo", default='efo')
    parser.add_argument("-u", "--user", type=str, help="set postgres user, default: postgres", default='postgres')
    parser.add_argument("-P", "--password", type=str, help="set user password - required")
    parser.add_argument("-pg", "--till_page", type=int, help="set page to be loaded upper limit - default: last ava", default=total_pages-1)
    args = parser.parse_args()

    config = vars(args)

    efoPipe(**config).run()

