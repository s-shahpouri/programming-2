import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import re


class Crawler:
    '''Crawler class that crawls the website sport050.nl and extracts the'''

    def __init__(self):
        '''Initializes the crawler class and sets the url, context, soup,'''
        self.url = "https://sport050.nl/sportaanbieders/alle-aanbieders/"
        self.ctx = self.hack_ssl()
        self.soup = self.open_url(self.url)
        self.reflist = self.read_hrefs(self.soup)
        self.sub_urls = self.get_sub_urls(self.reflist)
        self.current = 0

    @staticmethod
    def hack_ssl():
        """ ignores the certificate errors"""
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

    def open_url(self, url):
        """ reads url file as a big string and cleans the html file to make it
            more readable. input: url, output: soup object
        """
        html = urllib.request.urlopen(url, context=self.ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    @staticmethod
    def read_hrefs(soup):
        """ get from soup object a list of anchor tags,
            get the href keys and and prints them. Input: soup object
        """
        tags = soup('a')
        return [tag for tag in tags]

    @staticmethod
    def get_sub_urls(reflist):
        """Filter out the sub-urls from reflist"""
        sub_urls = [
            s for s in reflist if '<a href="/sportaanbieders' in str(s)]
        return sub_urls[3:]

    @staticmethod
    def read_li(soup):
        """ get from soup object a list of li tags """
        tags = soup('li')
        return [tag for tag in tags]

    def get_phone(self, info):
        """Extract phone number from info"""
        reg = r"(?:(?:00|\+)?[0-9]{4})?(?:[ .-][0-9]{3}){1,5}"
        phone = [s for s in info if 'Telefoon' in str(s)]
        if not phone:
            phone = [s for s in info if re.findall(reg, str(s))]
        return self.remove_html_tags(phone[0] if phone else "").replace('Facebook', '').replace('Telefoon:', '').strip()

    @staticmethod
    def get_email(info):
        """Extract email from soup"""
        email = [s for s in info if '@' in str(s)]
        if email:
            email_str = str(email[0])[4:-5]
            bs = BeautifulSoup(email_str, features="html.parser")
            return bs.find('a').attrs['href'].replace('mailto:', '')
        return ""

    @staticmethod
    def remove_html_tags(text):
        """Remove html tags from a string"""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    def fetch_sidebar(self, soup):
        """Fetches the sidebar of a soup object"""
        sidebar = soup.findAll(attrs={'class': 'sidebar'})
        return sidebar[0]

    def extract(self, url):
        """Extracts the necessary details from a url"""
        text = str(url)
        text = text[26:].split('"')[0] + "/"
        return text

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= len(self.sub_urls):
            raise StopIteration
        else:
            sub = self.extract(self.sub_urls[self.current])
            site = self.url[:-16] + sub
            soup = self.open_url(site)
            info = self.fetch_sidebar(soup)
            info = self.read_li(info)
            phone = self.get_phone(info)
            email = self.get_email(info)
            self.current += 1
            return f'{site} ; {phone} ; {email}'
