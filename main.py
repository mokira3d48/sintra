import os
import argparse
from sintra import main


if __name__ == '__main__':
    # Command line arguments parsing
    parser = argparse.ArgumentParser();
    parser.add_argument('impl', type=str, help="Option name.");
    parser.add_argument('url',  type=str, help="URL of WEB page that you want scrap.");
    args = parser.parse_args();

    # execution of main function
    exitcode = main(impl=args.impl, url=args.url);
    os.sys.exit(exitcode);


