import requests
import re
from bs4 import BeautifulSoup

class Scraper:
    def __init__ (self):
        self.session = requests.Session ()

        self.extensions = {
            'image': ['png', 'jpg', 'jpeg', 'gif'],
            'audio': ['mp3', 'm4a', 'aac'],
            'video': ['mkv', 'mp4', 'webm']
        }

    def get_html (self, url=None, local=False, binary=False):
        if local is True:
            return open("sample.html").read()
        try:
            response = self.session.get (url)
            response.raise_for_status()
        except requests.exceptions.MissingSchema as error:
            print (f"[ERROR]: Invalid URL: {url}")
        except requests.exceptions.HTTPError as error:
            print (error)
        else:
            return response.text if binary is False else response.content

        print("Exception Occured ....., can't fetch the requested page")
        return None

    def get_ilinks (self, url = None, local=False):
        soup = BeautifulSoup (self.get_html (url, local), 'html.parser')

        link_tags = soup.find_all ('a', attrs = {'href': re.compile ("^(/)")});
        links = set ()
        for link in link_tags:
            if link.attrs['href'] is not None and link['href'] not in links:
                links.add (link['href'])
        return list (links)

    def get_elinks (self, url = None, local=False):
        soup = BeautifulSoup (self.get_html (url, local), 'html.parser')
        link_tags = soup.find_all ('a', attrs = {'href': re.compile ("^(https|http|ftp)(://).*")})

        links = set ()
        if url is not None:
            links.add (url)

        for link in link_tags:
            if link.attrs['href'] is not None and link['href'] not in links:
                links.add (link['href'])
        return list (links)

    def get_links (self, url=None, lst=None, local=False):
        # lst is supposed to contain ['image', 'audio', 'video'] in that format
        # for every item of list, joining it's value items from self.extensions
        links = []
        if lst is not None:
            exts = ['|'.join (self.extensions[item]) for item in lst]
            exts = '|'.join (exts)

            print ("Resulting Regex Pattern: ", exts)

            # This approach, is not working over 'http://dl.upfdl.com/files/Series/Stranger%20Things/S01/'
            """
            for link in self.get_elinks (url, local):
                if re.search (f"({exts})$", link) is not None:
                    links.append (link)
            """
            soup = BeautifulSoup (self.get_html (url, local), 'html.parser')
            for item in soup.find_all ('a', attrs={'href': re.compile (f"({exts})$")}):
                links.append (item['href'])

        return links

    def form_submit (self, url, payload):
        response = self.session.post (url, data = payload)
        return response
        
def usage (): 
    print (f"[USAGE]: python {sys.argv[0]} <url>")

if __name__ == '__main__':
    import sys
    if len (sys.argv) < 2:
        usage()
        exit (1)
    scraper = Scraper()

    # print (scraper.get_html (html))
    local = False
    url = sys.argv[1]

    if (sys.argv[1] == '--file'):
        local = True
        url = sys.argv[2]
    #     print (scraper.get_ilinks(local=True))
    #     print (scraper.get_elinks(local=True))
    #     print (scraper.get_links (lst="image audio video".split(), local=True))
    # else:
    #     print (scraper.get_ilinks(sys.argv[1]))
    #     print (scraper.get_elinks(sys.argv[1]))
    #     links = scraper.get_links (url=sys.argv[1], lst="image audio video".split())
    #     print (links)

    ilinks = scraper.get_ilinks (url, local)
    elinks = scraper.get_elinks (url, local)
    links = scraper.get_links (url, lst="image audio video".split(), local = local)
