"""Keywords extracting

import kyx0


extract_key   = kyx0.KExtractor(
        lang=kyx0.Lang.FR, 
        pattern=kyx0.get_default_pattern()
)
keywords_dict = extract_key(eg)
print(INFO + "=> {}".format(keywords_dict))

"""

import enum
import spacy


# constantes d'etat
ERRO = '[ \033[91mERRO\033[0m ]  '
WARN = '[ \033[93mWARN\033[0m ]  '
INFO = '[ \033[94mINFO\033[0m ]  '
SUCC = '[ \033[32mSUCC\033[0m ]  '

'''
EN_MODEL = ('en_core_web_md');
FR_MODEL = ('fr_core_news_md');
EN_ALPHA = "0123456789abcdefghijklmnopqrstuvwxyz-'";
FR_ALPHA = "0123456789abcdefghijklmnopqrstuvwxyz-éù'èçàîêâïôüûë";
EXTRACT_PATTERN = None;
NLP      = None;
MTC      = None;
ALP      = None;
'''
SBT_AVR = 4


class Lang(enum.Enum):
    """Enumaration of available language
    """
    EN = (0x00f1, 'en_core_web_md',
          "0123456789abcdefghijklmnopqrstuvwxyz-'")
    FR = (0x00f2, 'fr_core_news_md',
          "0123456789abcdefghijklmnopqrstuvwxyz-éù'èçàîêâïôüûë")


class BaseExPattern(object):
    """Class of pattern that will be used during keyword extration.
    """

    def __call__(self):
        """This function must be reimplemented in the derivated class."""
        raise NotImplementedError(
            "Define __call__ function in your sub class."
            )


def get_default_pattern():
    """Fonction that return a quick default pattern.

    Returns:
        ExPattern: Return the default pattern class.
    """

    class ExPattern(BaseExPattern):
        """ Definition of subclass that represents a default pattern. """

        def __call__(self):
            wpat = {
                'IS_PUNCT': False, # No punctuation.
                'IS_SPACE': False, # No space that is between words.
                'IS_STOP':  False, # Remove the stop word.
                'POS': {'NOT_IN': ['SPACE',
                                   'VERB',
                                   'ADJ',
                                   'ADV',
                                   'AUX',]},
            }
            wspat = wpat.copy()
            wspat.update({'OP': '+'})
            adppat = {'POS': 'ADP'}
            adjpat = {'POS': 'ADJ', 'OP': '?'}
            detpat = {'POS': 'DET', 'OP': '?'}

            pattern1 = [wpat, adppat, detpat, wpat]
            pattern2 = [wspat]
            pattern0 = [wpat]
            return [pattern1, pattern2, pattern0]
    return ExPattern


class KExtractor:
    """Object that used to extract keywords from a text
    """

    def __init__(self, lang, pattern, sbt_avr=SBT_AVR):
        """Constructor of keywords extractor.
        Args:
            lang (:obj:`Lang`) selected language.
            pattern (:obj:`ExPattern`): Pattern configuration
                of word extraction.
            sbt_avr (float, optional): average sensibility.
                Default set to SBT_AVR value.
        """
        #: we load language from pipeline.
        self._nlp = spacy.load(lang.value[1])
        self._mtc = spacy.matcher.Matcher(self._nlp.vocab)
        """:obj:`spacy.matcher.Matcher`:
            we initialize the matcher object with NLP vocab."""

        self._alp = lang.value[2]
        """we define an alphabet of the selected language."""

        self._ptn = pattern  #: Pattern for word extraction.
        self._sbt = sbt_avr  #: Ratio of filtering.
        self._x = ''  #: Represent the previews enter.
        self._y = None
        """mixed: Represent the previous result of the previous enter."""

    @property
    def sensibility(self):
        """float: Return the defined ratio """
        return self._sbt

    @sensibility.setter
    def sensibility(self, value):
        self._sbt = value

    @staticmethod
    def _tokok(token, alpha):
        """Checking character.

        Function that used to check if each character of the text
        passed in argument is in language alphabet.

        Args:
            token (:obj:`Doc`): The instance of NLP doc representing text.
            alpha (str): The language alphabet.
        
        Returns:
            bool: if all charaters of the texte are contained in alpa,
            return True, else return False.
        """
        if len(token.text) > 1:
            for c in token.text:
                if c != ' ' and c.lower() not in alpha:
                    return False
            return True

    @staticmethod
    def _reg_counts(elem, dict_):
        """Function which update the counts.
        
        Args:
            elem (str): The word will be count.
            dict_ (dict of <str, int>): Count dictionary.
        
        Returns:
            dict: Return the dictionary of count.
        """
        if elem in dict_:
            dict_[elem] += 1
        else:
            dict_[elem] = 1
        return dict_

    def __call__(self, x):
        """Redefining of __call__ function.
        Returns:
            dict: Return {} if x is None else return the result.
        """
        try:
            if not x:
                return {}
            if x == self._x:
                return self._y

            NLP = self._nlp
            MTC = self._mtc
            PTN = (self._ptn())()  # print(INFO + "{}".format(PTN));
            ALP = self._alp
            ratio = self._sbt
            text = x

            MTC.add('mmat_01', PTN)
            doc = NLP(text)
            matches = MTC(doc)
            counts = {}

            # I count the token lemma
            for match_id, start, end in matches:
                span = doc[start:end]
                kws = ''
                if self._tokok(span, ALP):
                    if len(span) > 1:
                        kws = span.text
                    else:
                        dock = NLP(span.text)
                        kws = dock[0].lemma_

                    counts = self._reg_counts(kws.lower(), counts)

            # I sorte the dict before to continue
            counts = dict(sorted(counts.items(),
                                 key=lambda item: item[1], reverse=True))
            coun = list(counts.values())
            if len(coun) == 0: 
                return {}

            min_ = coun[-1]
            max_ = coun[0]
            stdd = max_ - min_  # print(stdd);
            avr = stdd / ratio  # print(avr);

            keywords = {}
            for token, count in counts.items():
                if count >= avr:
                    keywords[token] = count
                else:
                    break

            print(SUCC + "{} keywords found!".format(len(keywords)))
            self._x = x
            self._y = keywords
            return keywords
        except Exception as e:
            print(ERRO + "ERROR ==> {}".format(e.args[0]))
            return {}


