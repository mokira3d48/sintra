import os
import argparse
from .impl import KeywordExtraction


# Exit code constantes
EXIT_SUCCESS = 0;
EXIT_FAILURE = 84;

# list of command line
KWEX_IMPL = 'getkw';


def main(**kwargs):
    """ Main function that will be call when this module is the main """
    selected_impl = kwargs.get('impl');
    if selected_impl == KWEX_IMPL:
        kw_extraction = KeywordExtraction();
        if 'url' in kwargs:
            kw_extraction.set_param(url=kwargs['url']);

        kw_extraction.start();
        kw_extraction.join();
        # print(kw_extraction.results);
        kw_extraction.show();

    return EXIT_SUCCESS;


'''
if __name__ == '__main__':
    # Command line arguments parsing
    parser = argparse.ArgumentParser();
    parser.add_argument('impl', type=str, help="Option name.");
    parser.add_argument('url',  type=str, help="URL of WEB page that you want scrap.");
    args = parser.parse_args();

    # execution of main function
    exitcode = main(impl=args.impl, url=args.url);
    os.sys.exit(exitcode);
'''

