import os
import argparse
from sintra.base import exec_process


# Exit code constantes
EXIT_SUCCESS = 0;
EXIT_FAILURE = 84;


def main(args):
    """
    Main function definition in program.
    """
    res = exec_process(args);
    if res:
        return EXIT_SUCCESS;
    else:
        return EXIT_FAILURE;


if __name__ == '__main__':
    # Command line arguments parsing
    parser = argparse.ArgumentParser();
    parser.add_argument('name',  type=str, help="Option name.");
    parser.add_argument('url',   type=str, help="URL of WEB page that you want scrap.");
    parser.add_argument('--lev', type=int, help="Set the navigation level. Default value is 0.");
    parser.add_argument('--sen', type=float, help="Set the keyword extractor sensibility. Default set to 4.");
    parser.add_argument('--lang', type=str, help="Select a language.");
    args = parser.parse_args();

    # execution of main function
    exitcode = main(args);
    os.sys.exit(exitcode);


