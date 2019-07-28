
import logging
from datadog import loggingsetup
from datadog.pageview_report_saver import PageviewReportSaver

loggingsetup.init(logging.DEBUG)


def test_filepath():

    year = 2017
    month = 3
    day = 1
    hour = 0

    report_saver = PageviewReportSaver()
    path = report_saver.get_filepath(year=year,
                                     month=month,
                                     day=day,
                                     hour=hour)
    assert path == "/tmp/2017.03.01.00.report"

def test_save():

    data = {
        'm': [(1, 'hey')]
    }

    file_saver = PageviewReportSaver()
    file_saver.save_report_to_path(data=data, filepath="/tmp/testout")

# end
