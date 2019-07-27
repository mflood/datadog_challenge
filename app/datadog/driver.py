"""
    driver.py

    load config / parse args

"""

import argparse
import logging
import datetime
from datadog import loggingsetup


def year_argument(some_arg):
    # data is only available from 2015 to current year

    as_int = int(some_arg)
    if as_int < 2015 or as_int > datetime.datetime.now().year:
        raise TypeError("")
    return as_int

def hour_argument(some_arg):

    as_int = int(some_arg)
    if as_int < 0 or as_int > 24:
        raise TypeError("")
    return as_int

def parse_args(argv=None):
    """
        Parse command line args
    """
    parser = argparse.ArgumentParser(description="Main Driver for DataDog Challenge")

    parser.add_argument('-v',
                        action="store_true",
                        dest="verbose",
                        required=False,
                        help="Debug output")

    parser.add_argument("--year",
                        dest="year",
                        metavar='YYYY',
                        default=datetime.datetime.now().year,
                        required=False,
                        type=year_argument,
                        help="Year of data to analyze 2015 - present (default current year)")

    parser.add_argument("--hour",
                        dest="hour",
                        metavar='H',
                        default=datetime.datetime.now().hour,
                        type=hour_argument,
                        required=False,
                        help="Hour of data to analyze (default current hour)")

    results = parser.parse_args(argv)
    return results


def main():
    """
        Args 
    """

    arg_object = parse_args()

    if arg_object.verbose:
        loggingsetup.init(logging.DEBUG)
    else:
        loggingsetup.init(logging.INFO)



if __name__ == "__main__":
    main()

# end
