from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

#-------------------------------------------------------------------------------

def scrape_poem(poem_url):
    poem_page = urlopen(poem_url).read()
    soup = BeautifulSoup(poem_page)
    poem = ''
    poem_string = soup.find_all("div", 
                                {"class": "KonaBody" })[0].find_all('p')[0]
    poem_string = str(poem_string)[3:-4].replace('<br/>', ' ')
    return poem_string

def scrape_poems_index(poems_index_url):
    poems_index = urlopen(poems_index_url).read()    
    soup = BeautifulSoup(poems_index)
    pages = soup.find_all("div", {"class": "pagination"})
    if len(pages) == 0:
        return get_all_links(soup)
    
    pages = pages[0].find_all('a')
    result = {}
    cnt = 0
    for page in pages:
        page_link = 'https://www.poemhunter.com/'+page['href']
        page_soup = BeautifulSoup(urlopen(page_link))
        result.update(get_all_links(page_soup))
    return result

def get_all_links(page_soup):
    result = {}
    for link in page_soup.find_all('table')[0].find_all('a'):
        result[link.text] = 'https://www.poemhunter.com/'+link['href']
    return result

def get_poems(poems_index, max_poems=None):
    poems = {}
    for i, (title, poem_url) in enumerate(poems_index.items()):
        print('fetching', title, '...')
        try:
            poems[title] = scrape_poem(poem_url)
            print('OK')
        except:
            print('impossible to fetch')
        if i == max_poems-1:
            return poems
    return poems


#name_poet1="john-milton"
#name_poet2="ezra-pound"
#name_poet3="walt-whitman"
#file_name_poet1="1608_1674-john-milton"
#file_name_poet2="1885_1972-ezra-pound"
#file_name_poet3="1819_1892-walt-whitman"

#name_poet1="edgar-allan-poe"
#name_poet2="oscar-wilde"
#name_poet3="ambrose-bierce"
#file_name_poet1="1809_1849-edgar-allan-poe"
#file_name_poet2="1854_1900-oscar-wilde"
#file_name_poet3="1842_1913-ambrose-bierce"

#name_poet1="william-shakespeare"
#name_poet2="william-wordsworth"
#name_poet3="william-blake"
#file_name_poet1="1564_1616-william-shakespeare"
#file_name_poet2="1770_1850-william-wordsworth"
#file_name_poet3="1757_1827-william-blake"

name_poet1="rudyard-kipling"
name_poet2="thomas-hardy"
name_poet3="sylvia-plath"
file_name_poet1="1865_1936-rudyard-kipling5"
file_name_poet2="1840_1928-thomas-hardy5"
file_name_poet3="1932_1963-sylvia-plath5"



poems_index_poet1 = scrape_poems_index('https://www.poemhunter.com/'+name_poet1+'/poems/')
poems_index_poet2 = scrape_poems_index('https://www.poemhunter.com/'+name_poet2+'/poems/')
poems_index_poet3 = scrape_poems_index('https://www.poemhunter.com/'+name_poet3+'/poems/')

poems_poet1 = get_poems(poems_index_poet1, max_poems=60)
poems_poet2 = get_poems(poems_index_poet2, max_poems=60)
poems_poet3 = get_poems(poems_index_poet3, max_poems=60)

filepoet1 = open(file_name_poet1+'.txt', 'w')
json.dump(poems_poet1, filepoet1)
filepoet1.close()

filepoet2 = open(file_name_poet2+'.txt', 'w')
json.dump(poems_poet2, filepoet2)
filepoet2.close()

filePoet3 = open(file_name_poet3+'.txt', 'w')
json.dump(poems_poet3, filePoet3)
filePoet3.close()


