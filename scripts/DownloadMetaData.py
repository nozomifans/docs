# -*- coding: utf-8 -*-
"""
Download Open Image training data v5 meta

author: Le Yan
"""

import os
import re
from multiprocessing import Pool
from urllib.request import urlopen
from bs4 import BeautifulSoup

website = 'https://storage.googleapis.com/openimages/web/download.html'
# labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
# classes = {'div':['row', 'col-2 titlecol', 'col-4', 'col-sixteenth', 'col-12'], 'button':['button']}
notitle = {'Images'}

save_dir = '/data1/lyan/ImageAnalysis/20190714/OpenImage/Labels/'

def downloadurl(dname,url):
	if not os.path.isdir(save_dir+dname):
		if not os.path.isdir(save_dir+dname.split('/')[0]):
			os.mkdir(save_dir+dname.split('/')[0])
		os.mkdir(save_dir+dname)
	os.chdir(save_dir+dname)
	os.system('wget '+url)
	# if url.rsplit('.',1)[1] == 'zip':
	# 	fname = url.rsplit('/',1)[1]
	# 	os.system('unzip '+fname)
	# 	os.remove(save_dir+dname+'/'+fname)
	
html = urlopen(website).read()
soup = BeautifulSoup(html, features='lxml')  # 'html.parser'
row = soup.find('div', {"class": "row"})

flag = 0
for r in row.next_siblings:
	if r.name=='h2':
		if flag==0:
			flag=1
		else:
			break
	if r.name and 'class' in r.attrs and 'row' in r.attrs['class']:
		n1 = re.findall(r'\w+',r.find(attrs={'class':'col-2 titlecol'}).get_text())
		if len(n1)>0:  # not empty
			if ' '.join(n1) not in notitle:
				titlecol = ' '.join(n1)
				n2 = [re.findall(r'\w+',c.get_text())[0] for c in r.find_all(attrs={'class':['col-4','col-fifth']})]
				ncount = 0
				all_href = r.find_all('a')
				for l in all_href:
					dname = titlecol+'/'+n2[ncount]
					downloadurl(dname, l['href'])
					ncount += 1
		else:
			dname = titlecol+'/'+n2[ncount]
			all_href = [l['href'] for l in r.find_all('a')]
			for l in all_href:
				downloadurl(dname, l)
			ncount += 1
		
