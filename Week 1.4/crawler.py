import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import re


class Crawler:
    def __init__(self):
        self.pointer = -1  # pointer
        self.sub_urls = []  # Keep track
        self.url = "https://sport050.nl/sportaanbieders/alle-aanbieders/"  # Define the URL

    @staticmethod
    def hack_ssl():
        """ ignores the certificate errors"""
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

    @staticmethod
    def open_url(url):
        """ reads url file as a big string and cleans the html file to make it
            more readable. input: url, output: soup object
        """
        ctx = Crawler.hack_ssl()
        html = urllib.request.urlopen(url, context=ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    @staticmethod
    def read_hrefs(soup):
        """ get from soup object a list of anchor tags,
            get the href keys and and prints them. Input: soup object
        """
        # reflist = []
        # tags = soup('a')
        # for tag in tags:
        #     reflist.append(tag)
        reflist = [tag for tag in soup('a')]
        return reflist

    @staticmethod
    def read_li(soup):
        # lilist = []
        # tags = soup('li')
        # for tag in tags:
        #     lilist.append(tag)
        lilist = [tag for tag in soup('li')]

        return lilist

    @staticmethod
    def get_phone(info):
        reg = r"(?:(?:00|\+)?[0-9]{4})?(?:[ .-][0-9]{3}){1,5}"
        phone = [s for s in filter(lambda x: 'Telefoon' in str(x), info)]
        try:
            phone = str(phone[0])
        except:
            phone = [s for s in filter(
                lambda x: re.findall(reg, str(x)), info)]
            try:
                phone = str(phone[0])
            except:
                phone = ""
        return phone.replace('Facebook', '').replace('Telefoon:', '')

    @staticmethod
    def get_email(soup):
        try:
            email = [s for s in filter(lambda x: '@' in str(x), soup)]
            email = str(email[0])[4:-5]
            bs = BeautifulSoup(email, features="html.parser")
            email = bs.find('a').attrs['href'].replace('mailto:', '')
        except:
            email = ""
        return email

    @staticmethod
    def remove_html_tags(text):
        """Remove html tags from a string"""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    @staticmethod
    def fetch_sidebar(soup):
        """ reads html file as a big string and cleans the html file to make it
            more readable. input: html, output: tables
        """
        sidebar = soup.findAll(attrs={'class': 'sidebar'})
        return sidebar[0]

    @staticmethod
    def extract(url):
        text = str(url)
        text = text[26:].split('"')[0] + "/"
        return text

    def crawl_site(self):
        print('fetch urls')
        s = self.open_url(self.url)
        reflist = self.read_hrefs(s)

        print('getting sub-urls')
        # sub_urls = [s for s in filter(
        #     lambda x: '<a href="/sportaanbieders' in str(x), reflist)]
        # sub_urls = sub_urls[3:]
        self.sub_urls = [
            s for s in reflist if '<a href="/sportaanbieders' in str(s)][3:]

    def __iter__(self):
        return self

    def __next__(self):
        self.pointer += 1
        if self.pointer >= len(self.sub_urls):
            raise StopIteration
        sub = self.extract(self.sub_urls[self.pointer])
        site = self.url[:-16] + sub
        soup = self.open_url(site)
        info = self.fetch_sidebar(soup)
        info = self.read_li(info)
        phone = self.get_phone(info)
        phone = self.remove_html_tags(phone).strip()
        email = self.get_email(info)
        email = self.remove_html_tags(email).replace("/", "")
        return f'{site} ; {phone} ; {email}'
