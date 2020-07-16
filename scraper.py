import requests 
import lxml.html as html
import os
import datetime
import unicodedata

HOME_URL = 'https://www.clarin.com/'
XPATH_LINK_TO_ARTICLE = '//article[contains(@class,"content-nota")]/a/@href'
XPATH_TITLE = '//div[contains(@class,"title")]/h1[contains(@id,"title")]/text()'
XPATH_SUMMARY = '//div[contains(@itemprop,"description")]/h2/text()'
#XPATH_BODY = '//article[contains(@class,"article")]/p[not(@class)]/text()'
XPATH_BODY = '//div[contains(@class,"body-nota")]/p/text()'


def parse_notice(link, today):
    try:
        response = requests.get(HOME_URL+link)
        #print(f'PARSE NOTICE = {link} -  Request = {response.status_code}')
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"','')
                title = title.replace(':','')
                print(title)
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError as i:
                print(f'Error --- {i}')
                return

            with open(f'{today}/{title}.txt','w',encoding='utf-8') as f:
                #print(title)
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
                f.close
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        #print(response.text)
        if response.status_code ==200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            else:
                pass
            print(f'Tamagno de la lista = {len(links_to_notices)}')
            for link in links_to_notices:
                #print(link)
                parse_notice(link, today)

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)
        
def run():
    parse_home()


if __name__=='__main__':
    run()