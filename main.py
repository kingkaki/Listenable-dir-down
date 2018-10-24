# -*- coding: utf-8 -*-
# @Author: King kaki
# @Date:   2018-10-20 21:41:47
# @Last Modified by:   King kaki
# @Last Modified time: 2018-10-21 11:28:07
import re
import os
import sys
import requests
import urllib.parse



def index(baseurl):
	r = requests.get(baseurl)
	urls = re.findall(r'<a href="([^/][%a-zA-Z0-9_\./-]+?)">', r.text)
	return [baseurl+url for url in urls if url != '/']

def download(url, filename):
	if os.path.exists(filename):
		print("[exist]\t"+filename)
	else:
		print("[down]\t"+filename)
		r = requests.get(url)
		with open(filename, 'wb') as fd:
			for chunk in r.iter_content(1024):
				fd.write(chunk)

def mkdir(path):
	if not os.path.exists(path):
		os.makedirs(path) 
		print("[mkdir]\t"+path)
	else:
		print("[exist]\t"+path)



# print(urls)
# exit()

def main(baseurl, basedir, urls):
	for url in urls:
		# print(url)
		if url.endswith("/"):
			dirname = url.replace(baseurl,"")
			mkdir(basedir+dirname)

			urls = index(url)
			main(baseurl, basedir, urls)

		else:
			filename = url.replace(baseurl,"")
			filename = urllib.parse.unquote(filename)
			download(url, basedir+filename)
		
def prepare(url):
	if not url.endswith("/"):
		url+='/'

	basedir = re.sub(r'http[s]?://',"",url)
	basedir = basedir.replace("/",'.')
	mkdir(basedir)
	basedir = basedir[:-1]+'/'


	return basedir, url




if __name__ == '__main__':
	
	if len(sys.argv) != 2:
		print("useage : python3 {} url".format(sys.argv[0]))
		exit()
	else:
		basedir, baseurl = prepare(sys.argv[1])
		urls = index(baseurl)
		main(baseurl, basedir, urls)