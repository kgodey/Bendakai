========
Bendakai
========

Bendakai (http://bendakai.com) is a recipe storage and recommendation website
built on the Django framework. It is a work in progress.


Features in Progress
====================

See `Features Planned <https://github.com/kgodey/Bendakai/wiki/Features-Planned/>`_ 
Any comments or suggestions are appreciated.

Installation
============

Code that Bendakai uses that is not in this repository:

* `South <http://south.aeracode.org/>`_
* `oauth2 <http://pypi.python.org/pypi/oauth2/>`_
* `python-openid <http://pypi.python.org/pypi/python-openid>`_
* `python-sdk <https://github.com/facebook/python-sdk>`_

Bendakai uses Django 1.3, although you can use it with 1.2 if you serve
the static files in ``recipes/static/`` without using ``contrib.staticfiles``.
Bendakai uses the following Django contrib apps:

* ``django.contrib.auth``
* ``django.contrib.contenttypes``
* ``django.contrib.sessions``
* ``django.contrib.sites``
* ``django.contrib.admin``
* ``django.contrib.markup``
* ``django.contrib.comments``
* ``django.contrib.staticfiles``

For Facebook, Twitter and OpenID authentication to work, consult the
`django-socialregistration <https://github.com/flashingpumpkin/django-socialregistration>`_ documentation.

