import requests, csv
from datetime import datetime
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool

'''				PRACTICA WEB SCRAPPING 

			JORDI ORRIOLS/JORDI ABALLÓ


'''
n= 0


def addP(n):
	url= 'http://repertoire.bmi.com/PubContact.aspx?detail=pubid&page=1&fromrow=1&torow=25&keyid={}&subid=0'.format(n)
	while True:
		try:
			page = requests.get(url, timeout=60)
			if page.status_code == 404:
				return []
			break
		except:
			continue
	soup = BeautifulSoup(page.text, 'html5lib')
	disco = Disco(soup)
	name = Name(soup)
	phone = Phone(soup)
	return [disco, name, phone]

def Disco(soup):
	disco = soup.find('h1', attrs={'class': 'column-header'})
	if disco: 
		return disco.text.strip()
	else: return ''
	

def Name(soup):
	name = soup.find('td', attrs={'class': 'value'})
	if name:
		list1 =  name.text.strip().split('<br>')
		try:
			return list1[0]
		except:
			return name
	else: return ''

def Phone(soup):
	phone = soup.find('#contactTable')
	if phone:
		phone = phone.find('tr')[0].find('td')
		try:
			return str(phone[1])
		except:
			return phone
	else: return ''

def add2DB(file, disco, name, phone):
	with open('{}.csv'.format(file), 'a') as csv_file:
		if disco != '' and name != '' and phone != '':
			writer = csv.writer(csv_file)
			writer.writerow([disco, name, phone])
	return disco, name, phone

def getOne(n):
	return add2DB('test_final', *addP(n))

def __main__(n):
	with ThreadPool(8) as p:
		for disco, name, phone in p.imap_unordered(getOne, range(10**6)):
			print(f'{name} {disco} {phone}')

__main__(n)