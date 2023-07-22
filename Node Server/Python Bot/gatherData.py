import json
import time
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup as bf

settings = {
    'mainURL': 'https://www.shopflix.com.tr',
    'categoriesURL': '/kategoriler.html'
}

rawRequest = requests.get(settings['mainURL'] + settings['categoriesURL'])
html = bf(rawRequest.content, 'html.parser')

categories = html.select('div.filter-menu-main-category > a')
category_list = {category.text.strip(): {'categoryURL': settings['mainURL'] + category.get('href')} for category in categories}

CategorySession = requests.session()

for category in tqdm(category_list):
    try:
        categoryPage = CategorySession.get(category_list[category]['categoryURL'])
        categoryHTML = bf(categoryPage.content, 'html.parser')

        products = categoryHTML.select('div.showcase')

        if categoryHTML.select_one('div.paginate'):
            last_page = int(categoryHTML.select_one('div.paginate-content > a:last-child').text)
            if last_page > 1:
                for k in range(last_page):
                    cp = CategorySession.get(category_list[category]['categoryURL'] + "?tp=" + str(k+2))
                    ch = bf(cp.content, 'html.parser')
                    for h in categoryHTML.select('div.showcase'):
                        products.append(h)

        productsList = []
        for product in products:
            productURL = product.select_one('div.showcase-content > div.showcase-title > a').get('href')
            try:
                productBrand = product.select_one('div.showcase-content > div.showcase-brand > a').text
            except:
                productBrand = 'null'

            imgURL = None
            try:
                imgURL = product.select_one('img#primary-image').text
            except:
                imgURL = 'https://t4.ftcdn.net/jpg/04/73/25/49/360_F_473254957_bxG9yf4ly7OBO5I0O5KABlN930GwaMQz.jpg'

            productTitle = product.select_one('div.showcase-content > div.showcase-title > a').text
            productPrice = product.select_one(
                'div.showcase-content > div.showcase-price > div.showcase-price-new').text.strip()

            productsList.append({'productURL': productURL, 'productBrand': productBrand,
                                                   'productTitle': productTitle, 'productPrice': productPrice, 'productImageURL': imgURL})

            category_list[category]['products'] = productsList

        # print('Completed ', category)
        time.sleep(2)
    except Exception as e:
        print('Error in ', category)
        print(e)


with open('priceList.json', 'w') as priceList:
    priceList.write(json.dumps(category_list))