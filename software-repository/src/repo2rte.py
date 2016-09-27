#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# --- BEGIN_HEADER ---
#
# repo2rte - A helper to generate runtime environments from a sw repo
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

"""A parser to generate runtime environment info from packages in a SWRepo"""

import os
import sys
import urllib
from xml.dom import minidom

usage = '''This is a tool to extract central information about software
packages in a SWRepo online. It uses the RESTful SWRepo interface to find
and investigate all packages available in the repository. For each package
it parses the package description to extract the information for creating
a corresponding runtime environment (RTE).
Called with the URL of the SWRepo to use it generates and prints suggested
RTE information.
'''

repo_url = 'http://localhost:8080/package'

def list_packages(url, pattern='*'):
    """List all packages matching pattern from the repo"""
    all_packages = {}
    request = urllib.urlopen(os.path.join(url, pattern))
    matching = minidom.parse(request)
    request.close()
    #print matching.toxml()
    package_elems = matching.getElementsByTagName('package')
    attributes = ['name', 'href']
    for elem in package_elems:
        package = {}
        for field in attributes:
            package[field] = elem.getAttribute(field)
        all_packages[package['name']] = package
    return all_packages

def parse_package(url):
    """Extract central information from package description at url"""
    package = {}
    request = urllib.urlopen(url)
    all = minidom.parse(request)
    request.close()
    #print all.toxml()
    plain_fields = ['name', 'summary', 'description']
    for name in plain_fields:
        hits = all.getElementsByTagName(name)[0]
        package[name] = hits.childNodes[0].data
    return package


if __name__ == '__main__':
    if len(sys.argv) > 1:
        repo_url = sys.argv[1]
    try:
        awk_hits = list_packages(repo_url, '*awk')
        print awk_hits
    except Exception, exc:
        print "Error: in awk search: %s" % exc
    try:
        awk_info = parse_package(awk_hits.values()[0]['href'])
        print awk_info
    except Exception, exc:
        print "Error: in awk search: %s" % exc
    try:
        ssl_hits = list_packages(repo_url, '*ssl*')
        print ssl_hits
    except Exception, exc:
        print "Error: in awk search: %s" % exc
    try:
        ssl_info = parse_package(ssl_hits.values()[0]['href'])
        print ssl_info
    except Exception, exc:
        print "Error: in awk search: %s" % exc
                
