from .kyx0 import Lang
from .kyx0 import get_default_pattern
from .kyx0 import KExtractor
from .scripersite import URL
from .scripersite import Navigation
from .base        import register
from .base        import Processing
from . import INFO
from . import SUCC


@register(name='getkw')
class KeywordExtraction(Processing):
    """ 
    Keywords extraction implementation.
    """
    def __init__(self, *args, **kwargs):
        """ 
        Constructor of the keywords extraction program.
        """
        super(KeywordExtraction, self).__init__(*args, **kwargs);

    def run(self):
        """ 
        Function of execution of the program.
        """
        url_string = self._params.get('url', '');
        levelnav   = self._params.get('lev', 0);
        lang       = self._params.get('lang', 'en');
        sen        = self._params.get('sen', 4);

        url = URL(url_string);
        nav = Navigation(levn=levelnav);
        wbp = nav(url);
        # lines = wbp.find_all('p');
        # text  = " ".join([l.text for l in lines]);
        if wbp:
            if lang == 'en':
                lang = Lang.EN;
            elif lang == 'fr':
                lang = Lang.FR;
            else:
                lang = Lang.EN;
            sen = sen if sen else 4;
            print();
            print(INFO + "-> Language set to {}".format(lang));
            print(INFO + "-> Sensibility set to {}".format(sen));
            print(INFO + "Keyword extracting ... ");
            extract_key   = KExtractor(lang=lang, pattern=get_default_pattern());
            extract_key.sensibility = sen;
            keywords_dict = extract_key(wbp.get_text());
            self._results = keywords_dict;

    def show(self):
        """
        Function that is used to show the results
        """
        if self._results:
            k = 0;
            print();
            print("\033[36m%8s\t%32s\t%8s\033[0m" % ('INDEX', 'KEYWORDS', 'OCC'));
            for key, val in self._results.items():
                print("%8d\t%32s\t%8d" % (k + 1, key, val));
                k = k + 1;
        else:
            print(INFO + "No result.");

