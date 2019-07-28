"""
    args.py

    defines args for the program
"""

import sys
import datetime
import argparse

class ParserException(Exception):
    pass

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


def validate_args(args):
    """
        Does additional validation that is
        too complex for argparse
    """

    # exclusive or
    if bool(args.start_hour) != bool(args.end_hour):
        raise ParserException("Hour range requires --start-hour and --end-hour")

    if args.start_hour and args.end_hour < args.start_hour:
        raise ParserException("--end-hour cannot be less than --start-hour")

    # exclusive or
    if bool(args.start_date) != bool(args.end_date):
        raise ParserException("Date range requires --start-date and --end-date")

    if args.start_date and args.end_date < args.start_date:
        raise ParserException("--end-date cannot be less than --start-date")


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

    # range related options
    #
    range_group = parser.add_argument_group(title='Range Options')

    range_group.add_argument("--start-date",
                        dest="start_date",
                        metavar='YYYY-MM-DD',
                        required=False,
                        type=date_argument,
                        help="Start date of date range (inclusive)")

    range_group.add_argument("--end-date",
                        dest="end_date",
                        metavar='YYYY-MM-DD',
                        required=False,
                        type=date_argument,
                        help="End date of date range (inclusive)")

    range_group.add_argument("--start-hour",
                        dest="start_hour",
                        metavar='H',
                        type=hour_argument,
                        required=False,
                        help="Start of hour range (0-23)")

    range_group.add_argument("--end-hour",
                        dest="end_hour",
                        metavar='H',
                        type=hour_argument,
                        required=False,
                        help="End of hour range (0-23)")

    results = parser.parse_args(argv)

    try:
        validate_args(args=results)
    except ParserException as e:
        sys.stderr.write("{}\n".format(e))
        parser.print_help()
        sys.exit(2)

    return results

# end
