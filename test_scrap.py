import requests, csv
from datetime import datetime
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool

'''				<div class="col-sm-12 col-md-8">
					<div id="contentHeader" class="search-header">
					<span><h1 class="column-header">BIPO HIP HOP MUSIC</h1></span></div>
					<div id="affiliation" class="number-header">CAE/IPI #: 210512631</div>
					<div id="divContact"><table class="table" id="contactTable" border="0" cellpadding="0" cellspacing="0">
	<tr>
		<td><strong>Phone:</strong></td><td>(212) 893-9010</td>
	</tr><tr>
		<td><strong>Contact:</strong></td><td class="value">DAVID V ALMODOVAR<br>D/B/A BIPO HIP HOP<br>MUSIC<br>1550 TOWNSEND AVE APT 3-I<br>BRONX, NY 10452-6019</td>
	</tr>
</table></div>
					<div id="number_of_work_titles"></div>
					<div id="divCatalogLink" class="content-publisher-button"><a href="Catalog.aspx?detail=pubid&page=1&fromrow=1&torow=25&keyid=29358&subid=0" class="btn btn-primary pub-button">View Publisher's Catalog</a><br/></div>
					<div id="legend"></div>
				  </div>
'''

#29358
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