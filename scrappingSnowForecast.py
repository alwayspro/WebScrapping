import csv
import requests
from bs4 import BeautifulSoup



ESTACIONS = [
    {"nom": "Masella", "link": "https://es.snow-forecast.com/resorts/Masella/snow-report"},
    {"nom": "Panticosa", "link": "https://es.snow-forecast.com/resorts/Panticosa/snow-report"}
]

def get_info(estacio):
    data = {}
    data["nom"] = estacio["nom"]
    data["link"] = estacio["link"]
    page = requests.get(estacio["link"])
    print("Comença l'escraping de web")
    #print(page)

    soup = BeautifulSoup(page.content, 'html.parser')
    print("Fresh snow:")
    nevades = soup.find('span', class_='snow').get_text()
    data["nevades"] = nevades
    print(nevades)

    estado = soup.find('td', class_='value resort-runs').get_text()
    data["estado"] = estado
    print(estado)
    #report = soup.find_all('span',class_="report-key").parent
    #print(report)

    nevades=soup.find_all('div', class_='outer')
    maximNevada = nevades[1].get_text()
    minimNevada = nevades[0].get_text()
    data["maximNevada"] = maximNevada
    data["minimNevada"] = minimNevada

    return data


list_data = []
for estacio in ESTACIONS:
    data = get_info(estacio)
    list_data.append(data)
print(list_data)

with open('csvEstadoNive.csv', 'w') as f:
    myFields = ['nom', 'link', 'nevades','estado', 'maximNevada', 'minimNevada']
    writer = csv.DictWriter(f, fieldnames=myFields)
    writer.writeheader()
    for data in list_data:
        writer.writerow(data)

print("DONE")



