"""
    driver.py

    load config / parse args

"""

import argparse
import logging
import datetime
from datadog import loggingsetup

def make_date_from_string(date_string):
    """
        Given YYYY-MM-DD
        create a date object
    """
    year, month, day = date_string.split("-")
    date_object = datetime.date(int(year), int(month), int(day))
    return date_object

def date_argument(some_arg):
    # data is only available from 2015-05-01 to current year
    d = make_date_from_string(some_arg)

    if d < datetime.date(2015, 5, 1) or d > datetime.date.today():
        raise TypeError("")

    return d

def hour_argument(some_arg):

    as_int = int(some_arg)
    if as_int < 0 or as_int > 23:
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

    parser.add_argument("--date",
                        dest="date",
                        metavar='YYYY-MM-DD',
                        required=False,
                        type=date_argument,
                        help="Year of data to analyze 2015 - present (default current date)")

    parser.add_argument("--hour",
                        dest="hour",
                        metavar='H',
                        type=hour_argument,
                        required=False,
                        help="Hour of data to analyze (default current hour)")

    results = parser.parse_args(argv)
    return results


def make_url(date_object, hour):
    """
        return the appropriate wikimedia
        url for the given hour and year

        https://dumps.wikimedia.org/other/pageviews/2015/2015-05/pageviews-20150501-010000.gz
    """

    

def main():
    """
        Args 
    """

    arg_object = parse_args()

    if arg_object.verbose:
        loggingsetup.init(logging.DEBUG)
    else:
        loggingsetup.init(logging.INFO)

    logger = logging.getLogger(loggingsetup.LOGNAME)

    date_object =  arg_object.date
    if not date_object:
        date_object = datetime.date.today()

    hour = arg_object.hour
    if hour is None:
        hour = datetime.datetime.now().hour


    logger.info("date: {} hour: {}".format(date_object, hour))
    


if __name__ == "__main__":
    main()

# end
