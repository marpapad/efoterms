# efoterms


Tested with:
  - ubuntu 22.04
  - postgresql 14 installed
  - python 3.10 installed
  - pip3 22.0.2 installed
  
 user must have priviledges: create database, create table, select, update, insert
 user must have a password
 
 What it does:
  - installs necessary python packages (requirements.txt)
  - run main.py which does the following:
    * creates db an schema if not already exist (default efo, else the db given by the user)
    * loads the terms and their attibutes from the page and element not inserted in the db when executed the last time till the page defined by the user, if the upper limit is not defined then loads every available term

clone project

run </br>
$ cd /path/to/efoterms </br>
$ sudo chmod +x efo.sh </br>
$ ./efo.sh [-hs,--host= HOST, Optional, default: localhost] </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[-db,--db= DATABASE, Optional, default: efo] </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[-u,--user = USER, Optional, default: postgres] </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[-P,--password = PASSWORD, Optional, Required] </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[-pg,--till_page = PAGES TO BE RETRIEVED UPPER LIMIT, Optional, default: last available page] <\br>

<h3>example</h3>
<p>if we want to load into postres db efo (locally hosted) the terms till the page 20 using the user postgres whose password is intell1Pass we run the following:</p>
<p>$ ./efo.sh -P intell1Pass -pg 20</p>
