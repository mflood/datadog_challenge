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

    assert args.verbose == False
    assert args.hour == datetime.datetime.now().hour
    assert args.date == datetime.date.today()


def test_date():
    args = parse_args(["--date", "2019-04-04"])
    assert args.date == datetime.date(year=2019, month=4, day=4)

def test_invalid_date():
    """
        dates before 2015 are not allowed
    """
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        args = parse_args(["--date", "2014-04-04"])

def test_hour():
    args = parse_args(["--hour", "20"])
    assert args.hour == 20

def test_invalid_hour():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        args = parse_args(["--hour", "24"])
