# Ourblog
A Back-end project for a blog application

Four microservices that make up a blog web service. The service allows users to create accounts, publish articles, comment on articles, and add tags to articles. Additional features include:

* An Nginx reverse proxy to serve as a load balancer to distribute the requests between each microservice and their copies.
* An RSS feed that retrieves full articles, comments, or article summaries.

## Team Members
* Jeffrey Guerra
* Christian Jimenez
* Chloe Ho


# Things to install:

```pip3 install tavern```

```pip3 install foreman```

```sudo apt install python-pytest```

```sudo apt install ruby-foreman```

```sudo apt install --yes nginx-extras```

```sudo pip3 install Flask-BasicAuth```

```sudo apt install --yes docker.io```

```sudo usermod -aG docker $USER```

```sudo apt install --yes siege```

```sudo apt install --yes python3-cassandra```

# Setup #
Navigate to the project directory

## Commands ##
Create the databases: ```python3 create_dbs.py```

Start the services: ```python3 start.py```

Nginx configuration: Replace code in ```/etc/nginx/sites-enabled/default``` with code in the ```nginx-setup/sites-enabled-default``` file Once foreman has started, compare the ports for each service with the ports in the upstream portion of the nginx config file. Alter if necessary.

Start nginx: ```sudo service nginx restart```

RSS: Check the api docs for the RSS feeder for what URLs to hit.

Start Scylla: ```docker start scylla```

Check if scylladb is running: ```docker exec -it scylla nodetool status```


# Resources

HTTP Status Codes

https://www.restapitutorial.com/httpstatuscodes.html
Procfiles

https://mattstauffer.com/blog/using-a-procfile-to-streamline-your-local-development/
Nginx auth_request module

https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-subrequest-authentication/
