#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# --- BEGIN_HEADER ---
#
# swrepo - A RESTful software repository service 
# Copyright (C) 2009  The Grid.dk Project
#
# This file is part of SWRepo.
#
# SWRepo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# SWRepo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# -- END_HEADER ---
#

"""RESTful web service to interact with the grid.dk software repository:

Run as stand-alone server with:
./swrepo.py [FQDN] [PORT] [DOCROOT] [ACCESSENV] [ACCESSPATH ...] 
where FQDN and PORT are used for binding to the net, DOCROOT is the expected
document root and ACCESSENV and ACCESSPATH are for requiring the webserver
to limit access by checking if the value of the ACCESSENV environment variable
is included in the file(s) pointed to by ACCESSPATH. The latter can be a pickled
list of IDs or a raw list with one ID per line.

or

Run inside a WSGI capable web server like Apache with mod_wsgi and
WSGIScriptAlias /software-repository /path/to/swrepo.py

In that case the command line arguments are not supported so the configuration
must be edited directly in the site_conf dictionary below.

If swrepo runs inside a web server with SSL support the access control may use
client certificates by setting ACCESSENV to e.g. SSL_CLIENT_S_DN and the
ACCESSPATH to one or more files with acceptable client distinguished names.

Another possibility is to limit by IP with the REMOTE_ADDRESS environment.
"""

import os
import sys
import re
import fnmatch
import fcntl
import pickle
from ConfigParser import SafeConfigParser
from cgi import escape, FieldStorage

usage = '''<help>This is a RESTful interface for package repository management. 
Use HTTP GET with %(document_root)s/package?pattern=PATTERN to list all packages matching
PATTERN. Pattern may be a prefix or a wildcard pattern to search for.
Use HTTP POST with %(document_root)s/package?package=NAME;source=URL to bind package, NAME,
to download location, URL. Existing packages are updated the same way.
Providing an empty URL with an existing package NAME deletes the package.
</help>'''

# Site configuration - edit if running inside WSGI capable web server 

site_conf = {'site_name': 'grid.dk',
             'document_root': '/software-repository',
             'host': 'localhost',
             'port': 8080,
             'stand_alone': False,
             'access_env': 'SSL_CLIENT_S_DN',
             'access_paths': ['owners', 'members'],
             'repo_conf_path': 'repo.conf'}

# No more configuration past this point

site_conf['usage'] = usage % site_conf
cache = {}
# map actions to templates and urls to functions
templates = {'index': os.path.join('templates', 'index.xml'),
             'search': os.path.join('templates', 'package.xml'),
             'edit': os.path.join('templates', 'package.xml'),
             'interface': os.path.join('style', 'interface.xsl')}
urls= []

def read_packages():
    """Load all packages from conf"""
    repo_conf = SafeConfigParser()
    conf_fd = open(site_conf['repo_conf_path'], 'r')
    fcntl.flock(conf_fd, fcntl.LOCK_SH)
    repo_conf.readfp(conf_fd)
    fcntl.flock(conf_fd, fcntl.LOCK_UN)
    conf_fd.close()
    all_packages = {}
    for package in repo_conf.sections():
        entry = {}
        for (key, val) in repo_conf.items(package):
            entry[key] = val
        entry['package'] = package
        all_packages[package] = entry
    return all_packages

def write_packages(all_packages):
    """Save all packages to conf"""
    repo_conf = SafeConfigParser()
    for (package, entry) in all_packages.items():
        repo_conf.add_section(package)
        for (key, val) in entry.items():
            if key != 'package':
                repo_conf.set(package, key, val)
    conf_fd = open(site_conf['repo_conf_path'], 'w')
    fcntl.flock(conf_fd, fcntl.LOCK_EX)
    repo_conf.write(conf_fd)
    conf_fd.flush()
    fcntl.flock(conf_fd, fcntl.LOCK_UN)
    conf_fd.close()
    return True

def get_access_list():
    """Return access control list from site_conf setting:
    The access files may contain either a pickled list or multiple lines
    with one entry per line.
    """
    access_list = []
    for path in site_conf['access_paths']:
        try:
            access_fd = open(path, 'rb')
            acl_data = access_fd.read()
            access_fd.close()
        except:
            acl_data = ''
        try:
            acl = pickle.loads(acl_data)
        except:
            acl = acl_data.split('\n')
        access_list += [i for i in acl if i and not i in access_list]
    return access_list
        
def load_template(name):
    """Load template from memory or disk"""
    if not cache.has_key(name):
        template_fd = open(templates[name])
        cache[name] = template_fd.read()
        template_fd.close()
    return cache[name]

def response_headers(success=True, content_type='text/xml'):
    """Helper function to build default response headers"""
    if success:
        return ('200 OK', [('Content-Type', content_type)])
    else:
        return ('404 NOT FOUND', [('Content-Type', content_type)])

def interface(environ, start_response):
    """This function will be mounted on '%(document_root)s/interface.xsl' and 
    deliver a stylesheet to all subpages."""
    (status, headers) = response_headers(content_type='text/xsl')
    content = load_template('interface') % site_conf
    output = [content]
    start_response(status, headers)
    return output

def index(environ, start_response):
    """This function will be mounted on '%(document_root)s/' and display a link
    to all subpages."""
    site_conf['page_data'] = ''
    access_list = get_access_list()
    access_id = environ.get(site_conf['access_env'], '')
    method = environ['REQUEST_METHOD']
    if site_conf['access_env'] and not access_id in access_list:
        (status, headers) = response_headers(False, "text/plain")
        content = "No access for your client ID: '%s'" % access_id
    else:
        (status, headers) = response_headers()
        content = load_template('index') % site_conf

    output = [content]
    start_response(status, headers)
    return output

def search(environ, args, params):
    """Search available packages"""
    site_conf['page_data'] = ''
    # get the name from the url if it was specified there.
    if args:
        pattern = '%s*' % escape(args[0])
    elif params.has_key('pattern'):
        pattern = '%s*' % escape(params['pattern'][0])
    else:
        pattern = '*'
    if params.has_key('field'):
        search_field = '%s' % escape(params['field'][0])
    else:
        search_field = 'package'
    (status, headers) = response_headers()
    content = load_template('search')
    search_conf = {'pattern': pattern}
    lines = []
    lines.append('<search>%(pattern)s</search>' % search_conf)
    all_packages = read_packages()
    for (package, entry) in all_packages.items():
        if fnmatch.fnmatch(entry.get(search_field, ''), pattern):
            package_line = '<package href="%(source)s" name="%(package)s"/>'
            lines.append(package_line % entry)
    site_conf['page_data'] = '\n'.join(lines)
    content = content % site_conf
    return (status, headers, content)


def edit(environ, args, params):
    """Edit package"""
    site_conf['page_data'] = ''
    # get the name from the url if it was specified there.
    if args:
        package = '%s' % escape(args[0])
    elif params.has_key('package'):
        package = '%s' % escape(params['package'][0])
    else:
        package = '__UNSET__'
    if params.has_key('source'):
        source = '%s' % escape(params['source'][0])
    else:
        source = '__UNSET__'
    if params.has_key('owner'):
        owner = '%s' % escape(params['owner'][0])
    else:
        owner = 'ANYONE'
        
    content = load_template('edit')
    all_packages = read_packages()
    entry = {'package': package, 'source': source, 'owner': owner}
    if not package or '__UNSET__' == package:
        (status, headers) = response_headers(False)
        line = "Invalid or missing package '%(package)s'" % entry
    elif '__UNSET__' == source:
        (status, headers) = response_headers(False)
        line = "Missing source '%(source)s'" % entry
    else:
        valid = False
        package_owner = all_packages.get(package, {}).get('owner', 'ANYONE')
        owner_match = False
        if 'ANYONE' == package_owner or package_owner == owner:
            owner_match = True
        if not owner_match:
            line = 'You do not own package "%(package)s"' % entry
        elif source:
            valid = True
            all_packages[package] = entry
            line = 'Saved package "%(package)s" with source "%(source)s"' % entry
        elif all_packages.has_key(package):            
            valid = True
            del all_packages[package]
            line = 'Deleted package "%(package)s"' % entry
        else:
            line = 'No such package "%(package)s"' % entry
        (status, headers) = response_headers(valid)
        if valid:
            write_packages(all_packages)
    site_conf['page_data'] = "<edit>%s</edit>" % line
    content = content % site_conf
    return (status, headers, content)

def package(environ, start_response):
    """Handle all package operations using input variables and method"""
    # get the name from the url if it was specified there.
    args = environ['swrepo.url_args']
    # use basic cgi field parser with WSGI stdin and environment
    fields = FieldStorage(fp=environ['wsgi.input'], environ=environ,
                          keep_blank_values=True)
    parameters = {}
    for key in fields.keys():
        parameters[key] = fields.getlist(key)
    access_list = get_access_list()
    access_id = environ.get(site_conf['access_env'], '')
    method = environ['REQUEST_METHOD']
    if site_conf['access_env'] and not access_id in access_list:
        (status, headers) = response_headers(False, "text/plain")
        content = "No access for your client ID: '%s'" % access_id
    elif 'GET' == method:
        (status, headers, content) = search(environ, args, parameters)
    elif 'POST' == method:
        (status, headers, content) = edit(environ, args, parameters)
    else:
        (status, headers) = response_headers(False, "text/plain")
        content = "No handler for %s method" % method

    output = [content]
    start_response(status, headers)
    return output

def not_found(environ, start_response):
    """Called if no URL matches."""
    (status, headers) = response_headers(False, "text/plain")
    output = ['Not Found']
    start_response(status, headers)
    return output

def application(environ, start_response):
    """
    The main WSGI application. Dispatch the current request to
    the functions from above and store the regular expression
    captures in the WSGI environment as  `swrepo.url_args` so that
    the functions from above can access the url placeholders.

    If nothing matches call the `not_found` function.
    """
    # Standalone server holds URL in PATH_INFO instead of SCRIPT_URL
    if site_conf['stand_alone']:
        environ['SCRIPT_URL'] = environ.get('PATH_INFO', '')
        environ['SCRIPT_FILENAME'] = os.path.abspath(sys.argv[0])

    req_url = environ.get('SCRIPT_URL', '')
        
    # Extract abs script path and use to qualify relative paths
    exec_prefix = os.path.dirname(environ.get('SCRIPT_FILENAME', ''))
    site_conf['repo_conf_path'] = os.path.join(exec_prefix,
                                               site_conf['repo_conf_path'])
    site_conf['access_paths'] = [os.path.join(exec_prefix, i) \
                                for i in site_conf['access_paths']]
    for (name, rel_path) in templates.items():
        templates[name] = os.path.join(exec_prefix, rel_path)
    for regex, callback in urls:
        match = re.search(regex, req_url)
        if match is not None:
            environ['swrepo.url_args'] = match.groups()
            return callback(environ, start_response)
    return not_found(environ, start_response)

def get_urls():
    """Map URL's to functions"""
    urls = [
        (r'^%(document_root)s/$' % site_conf, index),
        (r'^%(document_root)s/package/?$' % site_conf, package),
        (r'^%(document_root)s/package/(.+)$' % site_conf, package),
        (r'^%(document_root)s/interface.xsl$' % site_conf, interface),
        ]
    return urls

# Always initialize urls - even if not running as dedicated server process

urls = get_urls()

if __name__ == '__main__':
    # Use command line arguments if running as stand-alone server
    from wsgiref.simple_server import make_server
    if len(sys.argv) > 1:
        site_conf['host'] = sys.argv[1]
    if len(sys.argv) > 2:
        site_conf['port'] = int(sys.argv[2])
    if len(sys.argv) > 3:
        site_conf['document_root'] = sys.argv[3].rstrip('/')
    if len(sys.argv) > 4:
        site_conf['access_env'] = sys.argv[4]
    if len(sys.argv) > 5:
        site_conf['access_paths'] = sys.argv[5:]
    urls = get_urls()
    site_conf['stand_alone'] = True
    srv = make_server(site_conf['host'], site_conf['port'], application)
    srv.serve_forever()
