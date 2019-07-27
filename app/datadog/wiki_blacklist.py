"""
    wiki_blacklist.py

    implements WikiBlacklist
    maintains globals BLACKLIST_URL and LOCAL_BLACKLIST_FILEPATH
"""

import logging
import os
import sys
import requests
from datadog.loggingsetup import LOGNAME

BLACKLIST_URL = "https://s3.amazonaws.com/dd-interview-data/data_engineer/wikipedia/blacklist_domains_and_pages"
LOCAL_BLACKLIST_FILEPATH = "/tmp/datadog_wiki_blacklist"


class WikiBlacklist():
    """
        Encapsulates blacklist
    """

    def __init__(self):
        self._logger = logging.getLogger(LOGNAME)
        self._blacklist = {}
        self._local_filepath = LOCAL_BLACKLIST_FILEPATH

    def get_size(self):
        """
            Return the number of items in the list
        """
        return len(self._blacklist)

    def head(self):
        """
            Show 20 entriew from the blacklist
        """
        keys = list(self._blacklist.keys())[:20]
        for k in keys:
            self._logger.info("blacklist %s = %s", k, self._blacklist[k])

    def _download_blacklist_file(self, url, local_filepath):
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
                        #self._logger.debug(len(chunk))
                        handle.write(chunk)


    def load_list(self, force_download=False):
        """
            possible download blacklist file
            and then parse it to load self._blacklist
        """
        if not os.path.exists(self._local_filepath) or force_download:
            self._download_blacklist_file(url=BLACKLIST_URL,
                                          local_filepath=self._local_filepath)
        self._blacklist = self._parse_file(local_filepath=self._local_filepath)
        self._logger.info("Loaded %d blacklist entries", len(self._blacklist))

    def _parse_file(self, local_filepath):
        """
            parses file, returns dictionary
            of the contents
        """
        self._logger.info("Loading blacklist data from %s", local_filepath)
        return_dict = {}
        with open(local_filepath, "r") as handle:
            for line in handle:
                line = line.strip()#.lower()
                return_dict[line] = 1

        return return_dict

    def is_blacklisted(self, page):
        """
            return true of page is in the blacklist
        """
        if page in self._blacklist:
            return True
        return False

# end
