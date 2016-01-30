# Linux Server Configuration
Baseline installation of a Linux distribution (Ubuntu 14.04.3 LTS) on a virtual server in Amazon's Elastic Compute Cloud (EC2) that hosts a Flash web application.

| IP address | SSH Port | URL |
| --- | --- | --- |
| 52.89.38.7 | 2200 | N/A |

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

libapache2-mod-wsgi is used in order for Apache to handle requests made from Python applications

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

## Port Configuration
1. Open the file sshd_config located in /etc/ssh/ `$ nano /etc/ssh/sshd_config`
2. Change port from 22 to 2200

## Setup SSH key authentication & disable password authentication
1. Temporarily allow password authentication by changing `PasswordAuthentication` fron no to yes
2. Restart ssh by typing `$ service ssh restart
3. On your local machine type: `$ ssh-keygen`
4. This will create a private and public key (.pub) in your .ssh folder in /home/username/.ssh
5. Copy the contents of the public key you created `$ cat public.pub`
6. Log into your virtual server under user grader
7. Create a folder named .ssh in your home directory `$ mkdrir .ssh`
8. Inside this folder create a file named `$ touch authorized_keys`
9. Paste the contents of the ssh public key you copied in the third step into authorized_keys `$ nano authorized_keys`
10. Disable password authentication by changing **PasswordAuthentication** from no to yes in sshd_config `$ sudo nano /etc/ssh/sshd_config`

## Firewall & Timezone Configuration
A good practice is to disable all connections (incoming/outgoing) before you start configuring your firewall.

1. First check if the firewall is enabled by typing `$ sudo ufw status`
2. If it is enabled disable it by typing `$ sudo ufw disable`
3. Disable all incoming connections `$ sudo ufw default deny incoming`
4. Disable all outgoing connections `$ sudo ufw default deny outgoing`
5. Allow incoming connections on port 2200 (SSH) `$ sudo ufw allow 2200/tcp`
6. Allow incoming connections on port 80 (HTTP) `$ sudo ufw allow 80/tcp`
7. Allow incoming connections on port 123 (NTP) `$ sudo ufw allow 123/udp`
8. Finally enable the firewall `$ sudo ufw enable`
9. You can check the status of UFW to see if everything is setup correctly `$ sudo ufw status`
10. Configure the local timezone to UTC `$ sudo timedatectl set-timezone UTC`

## Install & Configure Apache & mod_wsgi
1. Install Apache `$ sudo apt-get install apache2`
2. Confirm that Apache works by visiting your public IP. You'll see the "It works!" message
3. To run Python apps you need to install mod_wsgi `$ sudo apt-get install libapache2-mod-wsgi`

## Install Git
1. To install Git type: `$ sudo apt-get install git`

## Clone the application
1. Clone the application in your home directory
2. To clone the application type: `$ git clone https://github.com/kalpetros/projects.git`

## Install & Configure PostgreSQL

## Final Steps
The server is now configured and the application is ready to run.
Open your browser and visit the public IP. If you set up everything correctly you should be able to see the main page.

## Errors
If you get the following error when trying to install a package or update: 
> Could not resolve 'archive.ubuntu.com'
>
> W: Failed to fetch http://archive.ubuntu.com/...
>
> W: Some index files failed to download. They have been ignored, or old ones used instead.

check your firewall configuration.
Type: `$ sudo ufw default allow outgoing` and then try again.

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
