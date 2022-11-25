import threading as th

from .kyx0 import Lang
from .kyx0 import get_default_pattern
from .kyx0 import KExtractor
from .scripersite import URL
from .scripersite import Navigation


class KeywordExtraction(th.Thread):
    """ Keywords extraction implementation """

    def __init__(self, *args, **kwargs):
        """ Constructor of the keywords extraction program. """
        super(KeywordExtraction, self).__init__(*args, **kwargs);
        self._params  = {};
        self._results = None;

    @property
    def results(self):
        """ Return result of after program execution """
        return self._results;

    def set_param(self, **kwargs):
        """ Function that is used to set parametters of the program """
        self._params.update({name:val for name, val in kwargs.items()});
        return kwargs;

    def run(self):
        """ Function of execution of the program """
        url = URL(self._params.get('url', ''));
        nav = Navigation();
        wbp = nav(url);
        lines = wbp.find_all('p');
        text  = " ".join([l.text for l in lines]);
        extract_key   = KExtractor(lang=Lang.EN, pattern=get_default_pattern());
        keywords_dict = extract_key(text);
        self._results = keywords_dict;

    def show(self):
        """ Function that is used to show the results """
        if self._results:
            k = 0;
            print();
            print("%8s\t%32s\t%8s" % ('INDEX', 'KEYWORDS', 'OCC'));
            for key, val in self._results.items():
                print("%8d\t%32s\t%8d" % (k + 1, key, val));
                k = k + 1;
        else:
            print("No result.");


