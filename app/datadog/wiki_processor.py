"""
    wiki_processor.py

    implements WikiProcessor
"""

import logging
import gzip
import os
import heapq
import sys
import requests
from datadog.loggingsetup import LOGNAME

BASE_URL = "https://dumps.wikimedia.org/other/pageviews/"
CACHE_DIR = "/tmp"
TOP_N = 25
IGNORE_DASH = True

class WikiProcessor():
    """
        Knows how to download and process a wiki log file
    """

    def __init__(self, blacklist):
        self._logger = logging.getLogger(LOGNAME)

        # self._blacklist needs to implement is_blacklisted(page)
        self._blacklist = blacklist

    def get_url(self, year, month, day, hour):
        """
            return deterministic url filepath

            e.g.:

        https://dumps.wikimedia.org/other/pageviews/2015/2015-05/pageviews-20150501-010000.gz

        """
        path = "{base_url}/{y:04d}/{y:04d}-{m:02d}/pageviews-{y:04d}{m:02d}{d:02d}-{h:02d}0000.gz".format(
            base_url=BASE_URL.rstrip('/'),
            y=int(year),
            m=int(month),
            d=int(day),
            h=int(hour))
        return path

    def get_local_cache_path(self, year, month, day, hour):
        """
            return deterministic local filepath to cache the wiki data

            e.g. /tmp/2017.12.03.00.cache
        """
        path = "{}/{:04d}.{:02d}.{:02d}.{:02d}.cache".format(CACHE_DIR.rstrip('/'),
                                                             int(year),
                                                             int(month),
                                                             int(day),
                                                             int(hour))
        return path

    def _download_wiki_file(self, url, local_filepath):
        """
           Download a remote file to local_filepath
           Do it in chunks so we don't have the entire file in memory
        """
        self._logger.info("Downloading %s to %s", url, local_filepath)
        with requests.get(url, stream=True) as request:
            request.raise_for_status()
            with open(local_filepath, 'wb') as handle:
                for chunk in request.iter_content(chunk_size=8192):
                    if chunk: # filter out keep-alive new chunks
                        sys.stderr.write(".")
                        sys.stderr.flush()
                        handle.write(chunk)

    def process_pageviews(self, year, month, day, hour, force_download=False):
        """
            possibly download wiki file
            and then process it
            returning stats
        """
        local_path = self.get_local_cache_path(year, month, day, hour)

        if not os.path.exists(local_path) or force_download:
            url = self.get_url(year, month, day, hour)
            self._download_wiki_file(url=url,
                                     local_filepath=local_path)
        stats = self._process_file(local_filepath=local_path)
        return stats

    def _process_filehandle(self, filehandle):
        """
            given an open filehandle,
            process the file contents
        """

        stats = {}
        for index, raw_line in enumerate(filehandle):
            line = raw_line.strip().decode()
            #print("line is %s" % line)
            #print("type is %s" % type(line))
            parts = line.split(' ')

            stats.setdefault(parts[0], [])

            if IGNORE_DASH and parts[1] == '-':
                continue

            if not self._blacklist.is_blacklisted(page="{} {}".format(parts[0], parts[1])):
                # heapq can take a tuple like (2, 'something')
                # and will prioritize based on the first element
                # so we store (PAGEVIEWS, PAGE)
                # in the heap
                heapq.heappush(stats[parts[0]],
                               (int(parts[2]), parts[1]))

                # we want the heap to stay 25 elements
                # so we remove the lowest value
                # when it reaches 26
                if len(stats[parts[0]]) > TOP_N:
                    # remove the lowest value
                    heapq.heappop(stats[parts[0]])

        return stats

    def _process_file(self, local_filepath):
        """
            processes the localfile to gain stats
            parses file, returns dictionary
            of the stats

            expects the file is a gzipped file
        """
        self._logger.info("Loading page data from %s", local_filepath)

        with gzip.open(local_filepath, 'rb') as handle:
            return self._process_filehandle(handle)

# end
