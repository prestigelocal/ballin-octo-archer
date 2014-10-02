from multiprocessing import Process, Queue, Pool
from subprocess import call
import sys
import re, requests, json, codecs
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup as bs


# Takes URL, returns list of dictionarys containing url, rawHtml, and linkText
def crawl(URL):
	visited = [URL, "/"]
	html = []
	base = bs(requests.get(URL).content).prettify()
	html.append({"url":URL, "rawHtml":base})
	for a in bs(base).findAll("a"):
		try:
			if urlparse(a['href'])[2] not in visited and (urlparse(a['href'])[1] == "" or urlparse(a['href'])[1] == urlparse(URL)[1]):
				page = {}
				visited.append(re.sub("(?<!\:)/+", "/", URL + "/" + urlparse(a['href'])[2]))
				page['url'] = re.sub("(?<!\:)/+", "/", URL + "/" + urlparse(a['href'])[2])
				page['rawHtml'] = bs(requests.get(URL + '/' + urlparse(a['href'])[2]).content).prettify()
				page['linkText'] = a.text
				print "Found %s"%page['url']
				html.append(page)
		except:
			continue
	return html

def fork(toDo):
	url = "%s"%(toDo)
	f.write(json.dumps(crawl(line)))

if __name__ == '__main__':
	p = Pool(1)
	WebQueue = []
	i = 1
	for line in codecs.open("unclaimed.csv","r","utf-8"):
		WebQueue.append(line.strip())
	print WebQueue
	p.map(fork, WebQueue)

#f = codecs.open("webPage.txt", "w", "utf-8")
#f.write(json.dumps(crawl(line)))
