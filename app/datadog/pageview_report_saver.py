"""
    pageview_report_saver.py

    defines PageviewReportSaver
    maintains global REPORT_DIR

"""
import csv
import heapq
import logging
from datadog.loggingsetup import LOGNAME

REPORT_DIR = "/tmp/ddog_reports"

class PageviewReportSaver():
    """
        Knows how and where to save
        a pageviews report for a
        given year/month/day/hour
    """

    def __init__(self):
        self._logger = logging.getLogger(LOGNAME)

    def get_filepath(self, year, month, day, hour):
        """
            Determins the filepath based on
            year, monthm, day and hour
        """
        return "{}/{:04d}.{:02d}.{:02d}.{:02d}.report".format(
            REPORT_DIR.rstrip('/'),
            year,
            month,
            day,
            hour
        )

    def save_report_to_path(self, data, filepath):
        """
            Saves report to CSV
            ordered by domain, then pages ranked by num views
        """
        self._logger.info("Writing report to %s", filepath)
        with open(filepath, "w", newline='') as handle:
            fieldnames = ["domain", "page", "num_views"]
            csvwriter = csv.writer(handle,
                                   delimiter=',',
                                   quotechar='"',
                                   quoting=csv.QUOTE_MINIMAL)

            csvwriter.writerow(fieldnames)

            # write report in order of domains
            domains = list(data.keys())
            domains.sort()

            for domain in domains:
                views = data[domain]

                # views is a qheap of tuples
                # like
                # [ (20, 'page_A'), (10, 'page_B')
                # we can use qheap to pop them off
                # in numerical order
                sorted_list = []
                while views:
                    sorted_list.append(heapq.heappop(views))

                # we want the most views page at the top
                sorted_list.reverse()
                for item in sorted_list:
                    # item looks like (20, 'some page')
                    csvwriter.writerow([domain, item[1], item[0]])

# end
