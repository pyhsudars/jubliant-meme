#!/usr/bin/env python

from fabric.api import local


def run_wsgi(host="localhost", port=5000):
    print(local("gunicorn wsgi:app --bind {0}:{1}".format(host, port)))
