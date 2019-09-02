"""wsgiref -- a WSGI (PEP 3333) Reference Library

Current Contents:

* util -- Miscellaneous useful functions and wrappers

* headers -- Manage response headers

* handlers -- base classes for server/gateway implementations

* simple_server -- a simple BaseHTTPServer that supports WSGI
"""
import scrapy

class txtItem(scrapy.Item):
    link = None
    txtName = None
    content = None


