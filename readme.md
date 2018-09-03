Auth
====

Provides authentication services for other applications via HTTP request/response.

Usage
=====

Requirements
------------

* flask
* flask-sqlalchemy
* sqlalchemy

Configuration
-------------

You'll need to create a `config.py` file, which specifies details such as which LDAP
server to use. A sample configuration file can be found at `sample_config.py`.

Starting the Server
-------------------

Start the server with `run.py`. By default it will be accessible at `localhost:9999`. To
make the server world-accessible or for other options, see `run.py -h`.

If you're having trouble configuring your sever, I wrote a
[blog post](http://blog.spurll.com/2015/02/configuring-flask-uwsgi-and-nginx.html)
explaining how you can get Flask, uWSGI, and Nginx working together.

Bugs and Feature Requests
=========================

Feature Requests
----------------

None

Known Bugs
----------

None

License Information
===================

Written by Gem Newman. [Website](http://spurll.com) | [GitHub](https://github.com/spurll/) | [Twitter](https://twitter.com/spurll)

This work is licensed under Creative Commons [BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/).

Remember: [GitHub is not my CV](https://blog.jcoglan.com/2013/11/15/why-github-is-not-your-cv/).

