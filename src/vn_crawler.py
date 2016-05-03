#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This crawler accesses vndb pages and return images, links and other informations.
"""

import urllib3
import urllib3.contrib.pyopenssl

from lxml import etree

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED')
urllib3.contrib.pyopenssl.inject_into_urllib3()

VNDB_SITE = 'https://vndb.org'

def searchNovel(name):
    query = name.replace(' ', '+')
    url = VNDB_SITE+'/v/all?sq='+query
    r = http.request('GET', url, redirect=False)

    if r.status == 307:
        # Find only one, direct link
        return [(name, 'None', r.get_redirect_location())]
    html = etree.HTML(r.data)

    tr_nodes = html.xpath('//div["vnbrowse"]/table/tr')

    # tc1 - title, tc2/tc3 - icons/platforms, tc4 - release, tc5 - popularity, tc6 - rating
    return_list = []
    for node in tr_nodes:
        name = node.xpath('*[contains(@class, "tc1")]')[0][0].text
        rating = node.xpath('*[contains(@class, "tc6")]')[0].text
        link = VNDB_SITE + node.xpath('*[contains(@class, "tc1")]')[0][0].get('href')

        return_list.append((name, rating, link))

    return return_list
