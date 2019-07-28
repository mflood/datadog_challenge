"""
    test_wiki_processor.py

    unit tests for WikiProcessor
"""

import logging
import pytest
import requests_mock # pylint: disable=import-error
from datadog import loggingsetup
from datadog.wiki_processor import WikiProcessor
loggingsetup.init(logging.DEBUG)

SAMPLE_FILE = "tests/sample_pageviews.txt.Z"

def page_content(arg1, arg2):
    """
        Returns the binary content of
        tests/sample_pageviews.txt.Z
        to be returned by the mock request
    """
    with open(SAMPLE_FILE, "rb") as handle:
        content = handle.read()
    return content


@pytest.fixture()
def blacklist_mock():
    """
        Returns a mock WikiBlacklist
        that has a single item
        from tests/sample_pageviews.txt.Z blacklisted
    """

    class BlacklistMock():
        """
            Mock version of WikiBlacklist
        """

        def is_blacklisted(self, page):
            """
                Just blacklist one simple item
            """
            if page == "commons.m Category:1962_Flood_in_Skopje":
                return True

            return False

    return BlacklistMock()

@pytest.fixture()
def req_mock():
    """
        # info on requests mocking
        # usually requests_mock would be available as fixture
        https://requests-mock.readthedocs.io/en/latest/pytest.html
        # but requests_mock not available as fixture in python 3
        https://github.com/pytest-dev/pytest/issues/2749
        # hence, this fixture
    """
    with requests_mock.Mocker() as the_mocker:
        yield the_mocker


def test_get_url():
    """
        Test the get_url() method
    """
    processor = WikiProcessor(blacklist=None)
    url = processor.get_url(year=2017, month=12, day=3, hour=0)
    expected = "https://dumps.wikimedia.org/other/pageviews/2017/2017-12/pageviews-20171203-000000.gz"
    assert url == expected

def test_get_local_cache_path():
    """
        Test the get_local_cache_path() method
    """
    processor = WikiProcessor(blacklist=None)
    path = processor.get_local_cache_path(year=2017, month=12, day=3, hour=0)
    expected = "/tmp/2017.12.03.00.cache"
    assert path == expected

def test_process_pageviews(req_mock, blacklist_mock): # pylint: disable=redefined-outer-name
    """
        Test basic usage
        use mock to download fake contents
    """

    year = 2010
    month = 12
    day = 3
    hour = 0

    processor = WikiProcessor(blacklist=blacklist_mock)
    url = processor.get_url(year=year,
                            month=month,
                            day=day,
                            hour=hour)

    # this sets up the mock_url with a mock response
    req_mock.get(url, content=page_content)

    results = processor.process_pageviews(year=year,
                                          month=month,
                                          day=day,
                                          hour=hour,
                                          force_download=True)


    domains = list(results.keys())
    domains.sort()
    assert domains == ['as.m',
                       'bn.m',
                       'commons.m',
                       'commons.m.m',
                       'de',
                       'de.m',
                       'en',
                       'en.d',
                       'en.m',
                       'en.m.d',
                       'en.n',
                       'es',
                       'es.m',
                       'fr',
                       'fr.m',
                       'id.m',
                       'it',
                       'it.m',
                       'ja',
                       'ja.m',
                       'm.wd',
                       'no',
                       'pl',
                       'pt.m',
                       'ru.m',
                       'simple',
                       'simple.d',
                       'simple.m',
                       'sv.m',
                       'uk']



# end
