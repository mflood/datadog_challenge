#!/bin/sh 
date
source venv/bin/activate

# process hours 11, 12, 13 for 2019-02-27 through 2019-03-02
python3 datadog/driver.py --start-date=2019-02-27 --end-date=2019-03-02 --start-hour=11 --end-hour=13

date
