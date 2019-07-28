"""
    args.py

    defines args for the program
"""

import datetime
import argparse

def make_date_from_string(date_string):
    """
        Given YYYY-MM-DD
        create a date object
    """
    year, month, day = date_string.split("-")
    date_object = datetime.date(int(year), int(month), int(day))
    return date_object

def date_argument(some_arg):
    """
        Takes the date argument from the command line
        and converts it into a date object
        ensures the date is valid
    """
    # data is only available from 2015-05-01 to current date
    date_object = make_date_from_string(some_arg)

    if date_object < datetime.date(2015, 5, 1):
        raise TypeError("")

    return date_object

def hour_argument(some_arg):
    """
        Converts the hour passed on command line
        to int.  Validates.
    """
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
                        default=datetime.date.today(),
                        type=date_argument,
                        help="Year of data to analyze 2015 - present (default current date)")

    parser.add_argument("--hour",
                        dest="hour",
                        metavar='H',
                        required=False,
                        default=datetime.datetime.now().hour,
                        type=hour_argument,
                        help="Hour of data to analyze (default current hour)")

    results = parser.parse_args(argv)
    return results

# end
