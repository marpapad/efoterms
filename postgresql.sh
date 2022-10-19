#Update system packages
sudo apt -y update && upgrade
#Install PostgreSQL
sudo apt -y install postgresql postgresql-client
#Start PostgreSQL service
sudo service postgresql start
#Create user
sudo -i -u postgres psql -c "ALTER ROLE postgres WITH PASSWORD 'intell1Pass';"
#restart PostgreSQL service
sudo service postgresql restart
#re-install libpq for psycopg2
sudo apt-get -y install --reinstall libpq-dev