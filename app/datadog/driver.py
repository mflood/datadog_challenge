"""
    driver.py

    defines class Driver

    load config / parse args

"""

import logging
from datetime import timedelta
import os
from datadog import loggingsetup
from datadog.pageview_report_saver import PageviewReportSaver
from datadog.wiki_blacklist import WikiBlacklist
from datadog.wiki_processor import WikiProcessor
from datadog.args import parse_args


class Driver():
    """
        Coordinates the processor and report saver operations
    """

    def __init__(self, report_saver, wiki_processor):
        self._logger = logging.getLogger(loggingsetup.LOGNAME)
        self._report_saver = report_saver
        self._processor = wiki_processor

    def run_range(self, date_list, hour_list):
        """
            Runs report repeatedly
            for each date and for each hour
        """
        for date_object in date_list:
            for hour in hour_list:
                self.run_report(year=date_object.year,
                                month=date_object.month,
                                day=date_object.day,
                                hour=hour)

    def run_report(self, year, month, day, hour):
        """
            Runs the report for the
            given year, monthm, day and hour
        """
        self._logger.info("running report for %s %s %s %s",
                          year, month, day, hour)

        report_path = self._report_saver.get_filepath(year=year,
                                                      month=month,
                                                      day=day,
                                                      hour=hour)

        if os.path.exists(report_path):
            self._logger.warning("%s already exists. Skipping run.", report_path)
            return

        data = self._processor.process_pageviews(year=year,
                                                 month=month,
                                                 day=day,
                                                 hour=hour,
                                                 force_download=False)

        self._report_saver.save_report_to_path(data=data,
                                               filepath=report_path)


def hour_range_to_array(start_hour, end_hour):
    """
        Converts start/end hour to array of hours
    """

    logger = logging.getLogger(loggingsetup.LOGNAME)
    logger.info("Create hour range for %s - %s", start_hour, end_hour)
    if not start_hour and not end_hour:
        return None

    # argparse should validate these
    assert start_hour <= end_hour
    assert bool(start_hour) and bool(end_hour)

    return_array = []
    current_hour = start_hour
    while current_hour <= end_hour:
        return_array.append(current_hour)
        current_hour += 1

    return return_array

def date_range_to_array(start_date, end_date):
    """
        Converts start/end date to array of dates
    """
    logger = logging.getLogger(loggingsetup.LOGNAME)
    logger.info("Create date range for %s - %s", start_date, end_date)
    if not start_date and not end_date:
        return None

    # argparse should validate these
    assert start_date <= end_date
    assert bool(start_date) and bool(end_date)

    return_array = []
    current_date = start_date
    while current_date <= end_date:
        return_array.append(current_date)
        current_date += timedelta(days=1)

    return return_array


def main():
    """
        Args
    """
    arg_object = parse_args()

    if arg_object.verbose:
        loggingsetup.init(logging.DEBUG)
    else:
        loggingsetup.init(logging.INFO)

    # Create list of dates to process
    #
    date_array = date_range_to_array(arg_object.start_date,
                                     arg_object.end_date)
    # if there isn't a range, use the date arg
    if not date_array:
        date_array = [arg_object.date]

    # create list of hours to process
    #
    hour_array = hour_range_to_array(arg_object.start_hour,
                                     arg_object.end_hour)

    # if there isn't a range, use the hour arg
    if not hour_array:
        hour_array = [arg_object.hour]

    # create report_saver
    report_saver = PageviewReportSaver()

    # create blacklist
    blacklist = WikiBlacklist()
    blacklist.load_list(force_download=False)

    # create processor
    processor = WikiProcessor(blacklist=blacklist)

    # create driver
    driver = Driver(report_saver=report_saver,
                    wiki_processor=processor)

    # run reports
    driver.run_range(date_array, hour_array)

if __name__ == "__main__":
    main()

# end
