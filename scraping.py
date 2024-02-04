import requests
import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree
from datetime import datetime
import time

# Base URL of the website to scrape
url_base = 'https://listado.mercadolibre.cl/celulares'
# Start with the base URL
btn_siguiente = url_base
# Lists to store product names and prices
lista_nombres = []
lista_precios = []

# Use a while loop to iterate through pages up to the 5th
paginas_extraidas = 0
while paginas_extraidas < 5:
    # Make a request to the current page
    response = requests.get(btn_siguiente)
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract product names
    nombres = soup.find_all('h2', attrs={'class': 'ui-search-item__title'})
    nombres = [i.text for i in nombres]

    # Extract prices
    dom = etree.HTML(str(soup))
    precios = dom.xpath('//li[@class="ui-search-layout__item"]//div[@class="ui-search-result__content-columns"]//div[@class="ui-search-result__content-column ui-search-result__content-column--left"]/div[1]/div/div/div/span//span[@class="andes-money-amount__fraction"]/text()')

    # Check if the lists have the same length
    if len(nombres) != len(precios):
        print("The lists of names and prices do not have the same length. They will not be added to the final list.")
    else:
        lista_nombres.extend(nombres)
        lista_precios.extend(precios)

    print(btn_siguiente)

    # Find the link to the next page
    btn_siguiente_elem = soup.find('li', class_='andes-pagination__button--next')
    if btn_siguiente_elem and 'disabled' not in btn_siguiente_elem.get('class', []):
        btn_siguiente = btn_siguiente_elem.find('a').get('href')
    else:
        break

    paginas_extraidas += 1

    # Add a 1-second pause between each page request
    time.sleep(1)

# Create a Pandas DataFrame with the extracted information
df = pd.DataFrame({"Nombre": lista_nombres, "Precio": lista_precios})

# Add the Timestamp column
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
df["Timestamp"] = timestamp

# Save the DataFrame to an Excel file
df.to_excel("Datos_Celulares_MercadoLibre.xlsx", index=False)

