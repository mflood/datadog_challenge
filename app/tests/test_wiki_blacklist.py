"""
    test_wiki_blacklist.py

    unit tests for WikiBlacklist
"""

import logging
import pytest
import requests_mock # pylint: disable=import-error
from datadog import loggingsetup
from datadog.wiki_blacklist import WikiBlacklist
from datadog.wiki_blacklist import BLACKLIST_URL
loggingsetup.init(logging.DEBUG)

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

BLACK_LIST = """ab %D0%91%D0%BE%D1%80%D0%B8%D1%81_%D0%93%D1%80%D1%8B%D0%B7%D0%BB%D0%BE%D0%B2
ace Beureukaih:Nuvola_apps_important.svg
ace Japan
ace Kusuih:Hubong_gisa/Ureu%C3%ABng_Ngui:Hoo_User_Page_Bot
ace Kusuih:Neuubah_meuhubong/Seunaleu%C3%ABk:Flag
ace Marit_Ureu%C3%ABng_Ngui:GennadyL
ace.m Kusuih:MobileLanguages/Republik_Chuvash
af .sy
af 2009
af Apostelskap"""

def test_get_wiki_blacklist(req_mock): # pylint: disable=redefined-outer-name
    """
        Test basic usage
        use mock to download fake contents
    """

    # this sets up the mock_urtl with a mock response
    req_mock.get(BLACKLIST_URL, text=BLACK_LIST)

    wblk = WikiBlacklist()
    wblk._local_filepath = "/tmp/teapot"
    wblk.load_list(force_download=True)
    wblk.head()
    assert wblk.is_blacklisted(page="af Apostelskap")
    assert not wblk.is_blacklisted(page="af apostelskap")
    assert wblk.get_size() == 10

# end
