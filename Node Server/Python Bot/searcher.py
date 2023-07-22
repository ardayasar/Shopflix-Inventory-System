import json
from modules.priceExtractor import productSearch, priceExtractor

productSearch = productSearch()

dataFile = open('priceList.json', 'r').read()
data = json.loads(dataFile)


for category in data:
    for product in data[category]['products']:
        searchResults = productSearch.search(product['productTitle'])

        if len(searchResults) == 0:
            continue

        searchResults = searchResults[0]
        allProducts = searchResults['products']

        print([searchResults['totalCount']])
        print(product['productTitle'])
        for prod in allProducts:
            print(prod['price'])

# break

