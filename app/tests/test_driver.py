
import datadog.driver
import datetime

def test_date_range_to_array():

    results = datadog.driver.date_range_to_array(start_date=None, 
                                                end_date=None)

    assert results is None

    start = datetime.date(2019, 5, 30)
    end = datetime.date(2019, 6, 4)
    results = datadog.driver.date_range_to_array(start_date=start,
                                                 end_date=end)
    expected = [
        datetime.date(2019, 5, 30),
        datetime.date(2019, 5, 31),
        datetime.date(2019, 6, 1),
        datetime.date(2019, 6, 2),
        datetime.date(2019, 6, 3),
        datetime.date(2019, 6, 4),
    ]

def test_hour_range_to_array():

    results = datadog.driver.hour_range_to_array(start_hour=None, 
                                                 end_hour=None)

    assert results is None

    start = datetime.date(2019, 5, 30)
    end = datetime.date(2019, 6, 4)
    results = datadog.driver.hour_range_to_array(start_hour=8,
                                                 end_hour=13)
    expected = [ 8, 9, 10, 11, 12, 13]
    assert results == expected

def test_driver():

    class MockSaver():

        def get_filepath(self, year, month, day, hour):
            if hour == 4:
                # return a file that exists
                return "/tmp"

            return "/tmp/thisfiledoesnotexist"

        def save_report_to_path(self, data, filepath):
            pass


    class MockProcessor():
        pass
        def process_pageviews(self,
                              year,
                              month,
                              day,
                              hour,
                              force_download):
            data = {}

            return data

    driver = datadog.driver.Driver(report_saver=MockSaver(),
                                   wiki_processor=MockProcessor())


    hour_range = [3, 4] 
    date_range = [datetime.date(2019, 6, 2)]

    driver.run_range(date_list=date_range,
                     hour_list=hour_range)
