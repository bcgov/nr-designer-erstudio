import requests
from requests.auth import HTTPBasicAuth

from html.parser import HTMLParser
from erstudiolib.parameters import Parameters

class verParser(HTMLParser):
    '''
    Thisclass accesses the subversion website

    '''
    def __init__(self):
        HTMLParser.__init__(self)
        self.dat1 = None
        self.dat2 = None
        self.dat3 = None
        self.version = []

    def handle_data(self, data):
        self.dat3 = self.dat2
        self.dat2 = self.dat1
        self.dat1 = data
        self.vers = data

    def version_format(self, ver):
        result = ""
        numbers = ver.split('.')
        for num in numbers:
            result += num.zfill(3) + '.'
        return (result[:-1])

    def handle_starttag(self, tag, attributes):

        if tag != 'a':
            return
        if len(attributes) == 0:
            return
        u = attributes[0][1]
        if u != '../':
            self.version.append(self.version_format(u[:-1]))


class getAppVersionfromSVN():
    def __init__(self,app):
        self.svn_url = "http://repositories.nrs.gov.bc.ca/pub/svn/"  # returns an HTML table
        self.svn_app_url = f"{self.svn_url}/{app}/tags/"
        self.parms = Parameters()

    def version_format(self, ver):
        result = ""
        numbers = ver.split('.')
        for num in numbers:
            digit = num.lstrip("0")
            if len(digit) == 0:
                result += '0' + '.'
            else:
                result += digit + '.'
        return (result[:-1])

    def getversion(self):
        version = None
        s = requests.session()
        resp = s.get(self.svn_app_url, auth = HTTPBasicAuth(self.parms.username, self.parms.idirpass))
        if resp.status_code == 200:
            html = str(resp.content).replace("\\r","").replace("\\n","").replace("\\t","")[2:][:-1]
            htmlParse = verParser()
            htmlParse.feed(str(html))
            htmlParse.version.sort(reverse=True)
            if len(htmlParse.version) != 0:
                version = self.version_format(htmlParse.version[0])

        return(version)

