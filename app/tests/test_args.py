"""
    test_args.py

    test arg parser
"""
import datetime
import pytest
from datadog.args import parse_args


def test_defaults():
    """
        Defaults:

        verbose: false
        hour: current hour
        date: current date
    """
    args = parse_args([])

    assert not args.verbose
    assert args.hour == datetime.datetime.now().hour
    assert args.date == datetime.date.today()


def test_verbose():
    """
        verbose flag
    """
    args = parse_args(["-v"])
    assert args.verbose

def test_date():
    """
        datestring gets converted to date object
    """
    args = parse_args(["--date", "2019-04-04"])
    assert args.date == datetime.date(year=2019, month=4, day=4)

def test_invalid_date():
    """
        dates before 2015 are not allowed
    """
    with pytest.raises(SystemExit):
        parse_args(["--date", "2014-04-04"])

def test_hour():
    """
        hour is converted to int
    """
    args = parse_args(["--hour", "20"])
    assert args.hour == 20

def test_invalid_hour():
    """
        hour must be 0 <= hour <=23
    """
    with pytest.raises(SystemExit):
        parse_args(["--hour", "24"])

    with pytest.raises(SystemExit):
        parse_args(["--hour", "-1"])

def test_date_ranges():
    """
        date range must be legit
    """
    # incomplete range
    with pytest.raises(SystemExit):
        parse_args(["--start-date", "2019-04-01"])

    # incomplete range
    with pytest.raises(SystemExit):
        parse_args(["--end-date", "2019-04-01"])

    # start after end
    with pytest.raises(SystemExit) as some_error:
        parse_args(["--start-date", "2019-04-28",
                    "--end-date", "2019-04-01"])

def test_hour_ranges():
    """
        hour range must be legit
    """
    # incomplete range
    with pytest.raises(SystemExit):
        parse_args(["--start-hour", "2"])

    # incomplete range
    with pytest.raises(SystemExit):
        parse_args(["--end-hour", "2"])

    # start after end
    with pytest.raises(SystemExit):
        parse_args(["--start-hour", "4", "--end-hour", "2"])
