# Tech Challenge

Welcome to my humble tech challenge! I'll try to describe what I did, how I thought it, and what's this pile of code you'll be review. Fasten your seatbelt!

## Overview

First of all, the challenge details where pretty straight forward. So I thought drawing what I wanted to do was a good idea. Here's what came up:

![Image of Idea](https://i.ibb.co/W0Ky5tW/challenge.png)

So basically I'm using the required NGINX as an Api-Gateway (a fancy name for Reverse Proxy), routing HTTP traffic to the microservices hive. We have only one microservice in this example, but we'll zoom on it later.

On the other hand, the challenge asked for a way to configure "the server". So I thought... Which one is "the server"? The safiest assumption possible (an the most logic one) was the NGINX, so I took it. Therefore, you'll find a very simple playbook that changes the NGINX configuration based on a yml file, and then reloads it, without killing it.

All in all, let's dive in!

### Pre-requisites

You will need to install some stuff in order to make the app run. We need `docker` (of course) and `docker-compose`.
```
~ $ docker-compose --version
docker-compose version 1.26.0, build unknown
~ $ docker --version
Docker version 19.03.8, build afacb8b
~ $
```
If you don't have them, you can start your research on how to install `docker` in Ubuntu 18.04LTS [here](https://hub.docker.com/search?q=&type=edition&offering=community&operating_system=linux). For `docker-compose`, dive in [here](https://www.digitalocean.com/community/tutorials/how-to-install-docker-compose-on-ubuntu-18-04).

I strongly suggest to use `jq` aswell. It's a very tiny command-line json parser, that will make your life better. You can check how to install it [here](https://www.howtoinstall.me/ubuntu/18-04/jq/)

For the NGINX configuration part of this challenge, we'll use Ansible. I recommend installing it in a python virtual environment. You can get more info, and specific instrucions [here](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-ansible-with-pip).

### How I run it?

I tried to keep things simple: once you've cloned the repo (and solved the requisistes), just do a:
```
~ $ docker-compose up
```
This command will bring up all the stack:
- MySQL container
- Employees Microservice
- NGINX api-gateway

All the containers will come up at once, but *we need to wait until the data for the DB gets populated*. That takes a while, and until that finish, we are not able to use our app. This is a one time thing, as the data will be populated inside `mock_database/db_data`, and this directory is mapped into the DB container.

Once the population is completed, we can interact with it using a simple `curl`:
```
~ $ curl localhost:8080/employees | jq .
```
That we'll give us a JSON with the required information. Yey!

### What happend here?
Basically, we reached the NGINX container at `localhost:8080/employees`. This bad-boy is configured to 'proxy-pass' that URI to the `employees-ms` upstream. That uptream is pointing to our microservice container in the stack (on a different port), who is, at the very end, the one in charge of answering the request.

### The Api-gateway
As mentioned, this is an NGINX used as a reverse proxy: it will route all inconming HTTP traffic to different upstreams. The config files are separated in `nginx.conf`, which holds the main config, and `conf.d/locations.conf`, which has details about the `/employees` URI. It's an easy, but effective configuration.
I've set the server name in `ngnix.conf` as `_` to avoid adding a `Host` header to our `curl` commands.

### The microservice
Just make a quick close-up, the employees microservice is a simple Flask application, that make a quick SQL query:
```
select * from employees where gender = 'M' and birth_date = '1965-02-01' and hire_date > '1990-01-01' order by first_name ASC, last_name ASC;
```
That returns exactly what was asked in the challenge, but as a SQL object. After some manipulation, we get a really nice JSON based on a `collection.OrderedDict` object, to ensure that we deliver the information sorted out as requested.

### The DB
Nothing special here. Just a simple MySQL container. Something worth mentioning, is that I'm using `/docker-entrypoint-initdb.d` directory to populate the DB. That's an option that comes along with the container image: whatever you map as a volume into that container directory, will be run on start-up to help you fill up the database. [Here](https://hub.docker.com/_/mysql)'s some more extra information about that. Just search for *Initializing a fresh instance* section.

## Ansible
I've choosen Ansible to manage the NGINX configuration, as I'm confortable with its sintax, and been using it for a while now. The playbook `ansible/nginx-config.yml` will render the NGINX configuration templates, and reload the NGINX service inside the container. The templating is based on a `vars.yml` file that holds all the data needed to put them together. This way, you can easily add some new servers / locations to the NGNIX in a more controlled (and automated) way.

As told, in order to make this happen, you need to have Ansible installed. Once that's sorted out, you can go ahead and try this command: (remember to have the docker-compose stack running!)
```
~ $ cd ansible
~ ansible$ ansible-playbook nginx-config.yml
```
You'll notice that that the playbook output says something like: `TASK [run command in container]`. That's when the `service nginx reload` happens.
This is the best way I've found to emulate a productive scenario, in which we have the nginx running, and we need to alter its config without service interruption.


## Put together with:
* [Flask](https://palletsprojects.com/p/flask/) - WSGI web application framework.
* [Docker](https://www.docker.com/)
* [Ansible](https://www.ansible.com/resources/get-started)
* [Magic](https://media.giphy.com/media/12NUbkX6p4xOO4/giphy.gif)

## Authors
* **Chiqui** - *@ChiquiLandia*
