#!/usr/bin/python2.7
import requests
from BeautifulSoup import BeautifulSoup as BS
import time
import random

random.seed(time.time())

u_base = 'https://scholar.google.com'

u_search = '/citations?hl=en&view_op=search_authors&mauthors={}'

# gsc_prf_il for getting the domains of the author

f = open('authors.csv','r')
lines = f.readlines()
with open('authors_index.csv','w') as op:
    op.write("name, h_index, h_2013, i10, i10_2013, domains\n")
    for i in xrange(len(lines)):
        author = lines[i]
        # print author
        author = author.strip("\n")
        write_row = ""
        write_row += author+","
        auth = author.strip().split(" ")
        auth = "+".join(auth)
        # print auth
        url = u_base + u_search.format(auth)
        # print url
        response = requests.get(url)
        if response.status_code != 200:
            print author, response.reason
            break
        soup = BS(response.content)
        href = "take the first link"
        for text in soup.findAll(attrs={'class': 'gsc_oai_name'}):
            for links in text.findAll('a'):
                href = links.get('href')
        a_url = u_base + href
        time.sleep(random.random())
        result = requests.get(a_url)
        if result.status_code != 200:
            print author, response.reason
            break

        soup2 = BS(result.content)

        data = []
        table = soup2.find('table', attrs={'id':'gsc_rsb_st'})
        table_body = table.find('tbody')

        rows = table_body.findAll('tr')
        for row in rows:
            cols = row.findAll('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        write_row += "{},{},{},{},".format(data[1][1], data[1][2], data[2][1], data[2][2])
        domains = []
        for text in soup2.findAll(attrs={'class': 'gsc_prf_il', 'id' : 'gsc_prf_int'}):
            for link in text.findAll('a'):
                domains.append(link.getText())
        write_row += "{}\n".format(";".join(domains))
        op.write(write_row)
        if i%100 == 0:
            print "{} authors processed".format(i+1)
f.close()
