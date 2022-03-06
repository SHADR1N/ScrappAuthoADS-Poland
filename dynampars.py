from bs4 import BeautifulSoup as bs
import requests


base_url = 'https://www.olx.pl/motoryzacja/samochody/honda/jazz/'
headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0(X11;Linux x86_64...)Geco/20100101 Firefox/60.0'}

session = requests.session()
request = session.get(base_url, headers=headers)
if request.status_code == 200:
    
    soup = bs(request.content, 'html.parser')

    print(soup)
    ul = soup.find('div', class_='filter-item rel filter-item-model filterActive').find('ul')
    print(ul)
    for i in ul.findAll('li'):
    	print(i.text)







    # MainDiv = soup.find('ul', class_='_1rj80 _1sql3')
    # Div = MainDiv.findAll('li')
    # for i in Div:
    # 	print(i.text)

    # article = soup.findAll('div', class_='opbox-listing')[1].find('div').findAll('section')[1].findAll('article')

    # for o in article:
    # 	link = o.find('div')
    # 	price = link.find('div', class_='_9c44d_3AMmE')

    # 	url = link.find('a', class_='msts_9u mg9e_0 mvrt_0 mj7a_0 mh36_0 mpof_ki m389_6m mx4z_6m m7f5_6m mse2_k4 m7er_k4 _9c44d_1ILhl')
    # 	img = url.find('img')

    # 	print(img.get('src'))
