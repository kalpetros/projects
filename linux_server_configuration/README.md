# Linux Server Configuration
Baseline installation of a Linux distribution (Ubuntu 14.04.3 LTS) on a virtual server in Amazon's Elastic Compute Cloud (EC2) that hosts a Flash web application.
![](screenshot.png)

| IP address | SSH Port | URL |
| --- | --- | --- |
| 52.88.146.60 | 2200 | http://ec2-52-88-146-60.us-west-2.compute.amazonaws.com/ |

## What you'll be installing
To get the web application up and running the following need to be installed:
* Apache
* PostgreSQL
* python
* libapache2-mod-wsgi
* python-psycopg2 (Python PostgreSQL adapter)
* pip
* virtualenv
* Git
* Glances
* cron-apt

libapache2-mod-wsgi is used in order for Apache to handle requests made from Python applications

## IP to Hostname and Google Credentials setup
1. [Click here](http://www.hcidata.info/host2ip.cgi) and convert your public IP address to a hostname. For example this converts *25.16.26.9* to *cn-25-16-26-9.us-west-2.amazon.com*
2. To be able to use Google authentication you need to add the generated hostname to the Authorized JavaScript origins and Authorized redirect URIs. To do this [click here](https://console.developers.google.com/apis/credentials)

## Users
1. Add user grader
`$ adduser grader`
2. Give user grader sudo permissions. To do that open the file sudoers located in /etc/ `$ nano /etc/sudoers`
3. Once you opened the file you will something like the following:
```
# User privilege specification`
root    ALL=(ALL:ALL) ALL
# Enter here your user with his permissions
# For example:
grader  ALL=(ALL:ALL) ALL
```
1. Login under user grader
2. Disable root login. Open sshd_config located in /etc/ssh/ and change **PermitRootLogin without-password** to **PermitRootLogin no**
3. Restart the ssh service in order for changes to take effect: `$ sudo service ssh restart`
4. To test it out. Try and login under root and you'll get an error

## Port Configuration
1. Open the file sshd_config located in **/etc/ssh/**: `$ nano /etc/ssh/sshd_config`
2. Change port from 22 to 2200

## Setup SSH key authentication & disable password authentication
1. Temporarily allow password authentication by changing `PasswordAuthentication` fron no to yes
2. Restart ssh by typing: `$ service ssh restart`
3. On your local machine type: `$ ssh-keygen`
4. This will create a private and public key (.pub) in your .ssh folder in **/home/username/.ssh**
5. Copy the contents of the public key you created: `$ cat public.pub`
6. Log into your virtual server under user grader
7. Create a folder named .ssh in your home directory: `$ mkdrir .ssh`
8. Inside this folder create a file named: `$ touch authorized_keys`
9. Paste the contents of the ssh public key you copied in the third step into authorized_keys: `$ nano authorized_keys`
10. Disable password authentication by changing **PasswordAuthentication** from no to yes in sshd_config: `$ sudo nano /etc/ssh/sshd_config`

## Firewall & Timezone Configuration
A good practice is to disable all connections (incoming/outgoing) before you start configuring your firewall.

1. First check if the firewall is enabled by typing: `$ sudo ufw status`
2. If it is enabled disable it by typing: `$ sudo ufw disable`
3. Disable all incoming connections: `$ sudo ufw default deny incoming`
4. Disable all outgoing connections: `$ sudo ufw default deny outgoing`
5. Allow incoming connections on port 2200 (SSH): `$ sudo ufw allow 2200/tcp`
6. Allow incoming connections on port 80 (HTTP): `$ sudo ufw allow 80/tcp`
7. Allow incoming connections on port 123 (NTP): `$ sudo ufw allow 123/udp`
8. Finally enable the firewall: `$ sudo ufw enable`
9. You can check the status of UFW to see if everything is setup correctly: `$ sudo ufw status`
10. Configure the local timezone to UTC `$ sudo timedatectl set-timezone UTC`

## Setup Cron Job for automatic system updates
Automatically update the package list and download upgraded packages by using cron-apt

1. To install cron-apt type: `$ sudo apt-get install cron-apt`
2. Disable daily updates by commenting out the line: *0 4  * * * root test -x /usr/sbin/cron-apt && /usr-sbin/cron-apt* located in **/etc/cront.d/cron-apt**
3. To run weekly system updates go to /etc/cron.weekly and type: `$ sudo nano auto-update`
4. Paste the following and make it executable by typing: `$ chmod 755 auto-update`:
```
#!/bin/bash
apt-get update
apt-get upgrade -y
apt-get autoclean
```
#### Monitor repeated unsuccessful login attempts
1. Install fail2ban: `$ sudo apt-get install fail2ban`
2. Rename the default configuration file **jail.conf** located in **/etc/fail2ban/** to **jail.local**
3. Set bantime to 1800
4. Stop the fail2ban service: `$ sudo service fail2ban stop`
5. Start the fail2ban service: `$ sudo service fail2ban start`

## Install & Configure Apache & mod_wsgi
1. Install Apache: `$ sudo apt-get install apache2`
2. Confirm that Apache works by visiting your public IP. You'll see the "It works!" message
3. To run Python apps you need to install mod_wsgi: `$ sudo apt-get install python-setuptools libapache2-mod-wsgi`
4. Restart the Apache server in order to load mod_wsgi: `$ sudo service apache2 restart`

## Install Git
1. To install Git type: `$ sudo apt-get install git`

## Clone the application
1. Clone the application in your home directory
2. To clone the application type: `$ git clone https://github.com/kalpetros/projects.git`
3. Create a folder named catalog in **var/www/**
3. Move the application to **/var/www/catalog** and rename restaurants.py to `__init__.py`
4. Also rename the directory **item-catalog** to **catalog**

## Migrate from SQLite to PostgreSQL
1. Open **setup.py** located in **/var/www/catalog/catalog**
2. Change the line `engine = create_engine(sqlite:///restaurantsdb.db)` to this `engine = create_engine(postgresql://catalog:type_your_password_here@localhost/catalog)`
3. Create user catalog: `$ sudo adduser catalog`

## Deploying a Python application on Ubuntu VPS
1. Install additional Python packages: `$ sudo apt-get install python-dev`
2. Install pip: `$ sudo apt-get install python-pip`
3. Install virtualenv: `$ sudo pip install virtualenv`
4. Enable mod_wsgi: `$ sudo a2enmod wsgi`
5. Inside **/var/www/catalog/** create a file named catalog.wsgi: `$ sudo nano /var/www/catalog/catalog.wsgi` and paste the following:
```
#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/catalog/")
from catalog import app as application
application.secret_key = 'Add your secret key'
```
1. Create a **catalog.conf** file in **/etc/apache2/sites-available** in order to enable a new virtual host: `$ sudo nano /etc/apache2/sites-available/catalog.conf`
2. Inside **catalog.conf** paste the following:
```
<VirtualHost *:80>
  ServerName 52.89.38.7 # Replace with your public IP
  ServerAdmin admin@52.89.38.7 # Replace with your public IP
  ServerAlias ec2-52-89-38-7.us-west-2.compute.amazonaws.com # Replace with your url
  WSGIScriptAlias / /var/www/catalog/catalog.wsgi
  <Directory /var/www/catalog/catalog/>
    Order allow,deny
    Allow from all
  </Directory>
  Alias /static /var/www/catalog/catalog/static
  <Directory /var/www/catalog/catalog/static/>
    Order allow,deny
    Allow from all
  </Directory>
  ErrorLog ${APACHE_LOG_DIR}/error.log
  LogLevel warn
  CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```
1. Then cd to **/var/www/catalog/catalog/** and type: `$ sudo virtualenv venv`
2. Enable permissions for the new virtual environment: `$ sudo chmod -R 777 venv`
3. Then you need to source venv to be able to use it: `$ source venv/bin/activate`
4. Inside **/var/www/catalog/catalog** type: `$ pip install Flask sqlalchemy oauth2client requests Flask-SeaSurf dict2xml`
5. Deactivate venv: `$ deactivate`
6. Type: `$ sudo apt-get install python-psycopg2`
7. Enable the virtual host: `$ sudo a2ensite catalog`
8. Restart Apache server: `$ sudo service apache2 restart`

## Install & Configure PostgreSQL
1. Install PosgresSQL: `$ sudo apt-get install posgresql postgresql-contrib`
2. Login under user posgres: `$ sudo su - postgres`
3. Connect to PostgreSQL: `$ psql`
4. Create user catalog: `# CREATE USER catalog WITH PASSWORD 'type_your_password_here';`
5. Give permissions to user to create tables: `# ALTER USER catalog CREATEDB;`
6. Create database catalog: `# CREATE DATABASE catalog WITH OWNER catalog`;
7. Connect to database catalog: `# \c catalog`
8. Revoke all rights: `# REVOKE ALL ON SCHEMA public FROM public;`
9. Grant access only to catalog: `# GRANT ALL ON SCHEMA public to catalog;`
10. Exit: `# \q` & `$ exit`

## Setup the application
1. In **/var/www/catalog/catalog** execute **setup.py** in order to create the database schema: `$ python setup.py`
2. Populate the database: `$ python populate.py`
3. Restart Apache: `$ sudo service apache2 restart`

## Install Glances (monitoring tool)
1. Install glances `$ sudo pip install glances`
2. To run glances under Standalone Mode type `$ glances`
3. To remotely monitor this server type (on the server): `$ server -s`
4. On the client machine type: `$ glances -c @52.89.38.7

## Final Steps
The server is now configured and the application is ready to run.
Open your browser and visit the public IP or the url you created. If you set up everything correctly you should be able to see the main page.

## Errors
**Error 1** [Solution](https://help.ubuntu.com/community/UFW)

If you get the following error when trying to install a package or update: 
> Could not resolve 'archive.ubuntu.com'
>
> W: Failed to fetch http://archive.ubuntu.com/...
>
> W: Some index files failed to download. They have been ignored, or old ones used instead.

check your firewall configuration.
Type: `$ sudo ufw default allow outgoing` and then try again.

**Error 2** [Solution](https://discussions.udacity.com/t/cannot-connect-to-server-psql/46047/3?u=kalpetros)

> psql: could not connect to server: Permission denied
>
> Is the server running locally and accepting
>
> connections on Unix domain socket "/var/run/postgresql/.s.PGSQL.5432"?

**Error 3** [Solution](https://discussions.udacity.com/t/cannot-connect-to-server-psql/46047/3?u=kalpetros)

> * No PostgreSQL clusters exist; see "man pg_createcluster"

**Error 4** [Solution](https://discussions.udacity.com/t/cannot-connect-to-server-psql/46047/3?u=kalpetros)
```
locale: Cannot set LC_ALL to default locale: No such file or directory
LANG=en_US.UTF-8
LANGUAGE=
LC_CTYPE="en_US.UTF-8"
LC_NUMERIC=el_GR.UTF-8
LC_TIME=el_GR.UTF-8
LC_COLLATE="en_US.UTF-8"
LC_MONETARY=el_GR.UTF-8
LC_MESSAGES="en_US.UTF-8"
LC_PAPER=el_GR.UTF-8
LC_NAME=el_GR.UTF-8
LC_ADDRESS=el_GR.UTF-8
LC_TELEPHONE=el_GR.UTF-8
LC_MEASUREMENT=el_GR.UTF-8
LC_IDENTIFICATION=el_GR.UTF-8
LC_ALL=
```
## Sources
* [Configuring timezones](http://askubuntu.com/a/594186/145133)
* [How to add/delete users](https://www.digitalocean.com/community/tutorials/how-to-add-and-delete-users-on-an-ubuntu-14-04-vps)
* [List, add, delete, modify users](https://askubuntu.com/questions/410244/a-command-to-list-all-users-and-how-to-add-delete-modify-users)
* [How to grant sudo privileges to an existing user](https://askubuntu.com/questions/168280/how-do-i-grant-sudo-privileges-to-an-existing-user)
* [How to restart SSH](http://www.cyberciti.biz/faq/howto-restart-ssh/)
* [UFW - Uncomplicated Firewall](https://help.ubuntu.com/community/UFW)
* [Configure an SSH key-based authentication](https://www.digitalocean.com/community/tutorials/how-to-configure-ssh-key-based-authentication-on-a-linux-server)
* [Why am I getting authentication errors for packages from an Ubuntu repo](https://askubuntu.com/questions/75565/why-am-i-getting-authentication-errors-for-packages-from-an-ubuntu-repository)
* [How to deploy a Flask application on an Ubuntu VPS](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)
* [Install & Configure PostgreSQL](https://help.ubuntu.com/community/PostgreSQL)
* [How to secure PostgreSQL on an Ubuntu VPS](https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps)
* [ImportError: No module named psycopg2](https://stackoverflow.com/questions/12906351/importerror-no-module-named-psycopg2)
* [Delete rows of a table](http://www.postgresql.org/docs/8.2/static/sql-delete.html)
* [Convert Host/Domain name to IP address and vice versa](http://www.hcidata.info/host2ip.cgi)
* [How do I fix my locale issue?](https://askubuntu.com/questions/162391/how-do-i-fix-my-locale-issue)
* [Why won't PostgreSQL 9.3 start on Ubuntu?](https://dba.stackexchange.com/questions/50906/why-wont-postgresql-9-3-start-on-ubuntu)
* [Solving "No PostgreSQL clusters exist; see "man pg_cleatecluster" warning](http://solutions4linux.blogspot.gr/2014/09/solving-no-postgresql-clusters-exist.html)
* [How to check if service is running or not on Ubuntu?](https://stackoverflow.com/questions/18721149/how-to-check-service-is-running-or-not-on-ubuntu)
* [Cannot connect to server (psql)](https://discussions.udacity.com/t/cannot-connect-to-server-psql/46047/3?u=kalpetros)
* [Glances (monitoring tool)](https://glances.readthedocs.org/en/latest/glances-doc.html#introduction)
