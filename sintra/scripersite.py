import threading as th
import requests
import bs4


# constantes d'etat
ERRO = '[ \033[91mERRO\033[0m ]  ';
WARN = '[ \033[93mWARN\033[0m ]  ';
INFO = '[ \033[94mINFO\033[0m ]  ';
SUCC = '[ \033[32mOK\033[0m ]    ';


class URL:
    """ Structure of an URL """

    def __init__(self, val=''):
        """ Constructor of an URL """
        self._val = val;

    @property
    def value(self):
        """ Return the value of the URL """
        return self._val;

    @property
    def isempty(self):
        """ Return True if the URL is empty """
        return True if self._val else False;

    def __str__(self):
        """ Function of representation of URL in string. """
        return self._val;


class WebPage(bs4.BeautifulSoup):
    """ Structure and features of WEB page """

    def __init__(self, url: URL, content: str, **kwargs):
        """ Constructor of a web page """
        super(WebPage, self).__init__(content, 'html.parser', **kwargs);
        self._murl    = url;
        self._content = content;

    @property
    def url(self):
        """ Return URL of WEB page. """
        return self._murl;

    @property
    def content(self):
        """ Return the content of WEB page. """
        return self._content;

    def __str__(self):
        """ Function of representation of a WEB page in string. """
        return self._content;


class Navigation(th.Thread):
    """ Navigation thread definition """

    def __init__(self, *args, **kwargs):
        """ Constructor of a navigation thread. """
        super(Navigation, self).__init__(*args, **kwargs);
        self._wps  = {};
        self._curl = '';
        self._levn = 1;

    @property
    def url(self):
        """ Return the current URL of this nativation """
        return self._curl;

    @url.setter
    def url(self, value: URL):
        """ Set a value of current URL """
        self._curl = value;

    @property
    def level(self):
        """ Return the value of navigation level. """
        return self._levn;

    @level.setter
    def level(self, value):
        """ Define the navigation level """
        self._levn = value;

    @property
    def webpages(self):
        """ Return the dictionnary of web page indexed by URLs """
        return self._wps;

    def __call__(self, url: URL):
        """
        Function that is used to execute a navigation to a website using a URL. 

        :param: url [URL]  The URL that index a website that want to retreive.
        :return:
            [WebSite]
            We return an instance of WebSite found at the URL passed in argument.
        """
        print(INFO + "Navigation to {} ...".format(url));
        response = requests.get(url.value);
        if response.status_code == 200:
            # check status code for response received
            # success code - 200
            print(SUCC + "STATUS CODE - 200");
            return WebPage(url=url, content=response.content);
        else:
            # Cas of status code is different of 200
            print(ERRO + "STATUS CODE RETURNED - {}".format(response.status_code));
            return 0;

    def run(self):
        pass;


class WSNavigator:
    pass;


if __name__ == '__main__':
    url = URL('https://www.geeksforgeeks.org/python-web-scraping-tutorial/');
    nav = Navigation();
    wbp = nav(url);
    lines = wbp.find_all('p');
    for line in lines:
        print(line.text);
    


