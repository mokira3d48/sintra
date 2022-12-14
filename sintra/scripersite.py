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
        if self._val == '#':
            return '#';
        else:
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
        self._subwps  = [];
        self._layer   = 0;

    @property
    def url(self):
        """ Return URL of WEB page. """
        return self._murl;

    @property
    def content(self):
        """ Return the content of WEB page. """
        return self._content;

    @property
    def sub_web_pages(self):
        """ Return the list of registried sub web page. """
        return self._subwps;

    def register_subwebpage(self, wb):
        """ 
        Function used to register a sub web page in this.
        """
        if not isinstance(wb, WebPage):
            raise ValueError("wb argument must be a WebPage instance.");

        wb.__setattr__('_layer', self._layer + 1);
        self._subwps.append(wb);
        return wb;
    
    def get_text(self):
        text = super(WebPage, self).get_text();
        if self._subwps:
            for w in self._subwps:
                text += '\n' + w.get_text();
        return text;

    def __str__(self):
        """ Function of representation of a WEB page in string. """
        return self._content;


class Navigation(th.Thread):
    """ Navigation thread definition """

    def __init__(self, *args, levn=0, **kwargs):
        """ Constructor of a navigation thread. """
        super(Navigation, self).__init__(*args, **kwargs);
        self._wps  = {};
        self._curl = '';
        self._levn = levn if levn is not None\
            else 0;  ''' Define the level of the navigation on web page '''

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
        if value < 0:
            raise ValueError("The navigation level cannot be a nigative integer.");
        self._levn = value;

    @property
    def webpages(self):
        """ Return the dictionnary of web page indexed by URLs """
        return self._wps;

    def __call__(self, url: URL):
        """ 
        Redifinied function to call the navigation function when it called.
        """
        print(INFO + "Navigation level : {}".format(self._levn));
        print(INFO + "Navigation to {} ...".format(url));
        return self._nav(url, 0);

    def _nav(self, url: URL, lev: int=None):
        """
        Function that is used to execute a navigation to a website using a URL. 

        :param: url [URL]  The URL that index a website that want to retreive.
        :return:
            [WebSite]
            We return an instance of WebSite found at the URL passed in argument.
        """
        try:
            response = requests.get(url.value);
            if response.status_code == 200:
                # check status code for response received
                # success code - 200
                webpage = WebPage(url=url, content=response.content);
                self._wps[url] = webpage;
                print(SUCC + "STATUS CODE - 200 | {} is scrapped.".format(url));
                
                if type(lev) is int and lev < self._levn:
                    levn  = lev + 1;
                    atags = webpage.find_all('a');
                    if atags:
                        for a in atags:
                            surl = a.get('href');
                            if url and type(surl) is str and surl[0] != '#':
                                wp = self._nav(URL(surl), levn);
                                if wp:
                                    webpage.register_subwebpage(wp);
                return webpage;
            else:
                # Cas of status code is different of 200
                print(ERRO + "STATUS CODE RETURNED - {} for {}".format(response.status_code, url));
                return 0;
        except Exception as e:
            print(ERRO + "Error message: {}".format(e));
            return 0;

    def run(self):
        """ Redefining of run function of the Thread """
        self(self._curl);


class WSNavigator:
    pass;


if __name__ == '__main__':
    # url = URL('https://www.geeksforgeeks.org/python-web-scraping-tutorial/');
    url = URL('https://beautiful-soup-4.readthedocs.io/en/latest/');
    # url = URL('https://duckduckgo.com/?q=BeautifulSoup+document&ia=web/');
    nav = Navigation(levn=0);
    wbp = nav(url);
    # lines = wbp.find_all('p');
    # for line in lines:
    #     print(line.text);
    print("\n");
    print(INFO + "{} WEB PAGE(S) SCRAPPED !".format(len(nav.webpages)));
    print(wbp.get_text());
    # print(wbp.url, [w.url for w in wbp.sub_web_pages]);
    # for w in wbp.sub_web_pages:
    #    print(INFO + "{} WEB PAGE(S) SCRAPPED !".format(len(w.sub_web_pages)));
    
    


