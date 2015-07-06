__author__ = 'dev'

import pandas as pd
from dateutil import rrule

from zipline.utils.tradingcalendar import end, canonicalize_datetime


start = pd.Timestamp('2013-01-01', tz='UTC')
end_base = pd.Timestamp('today', tz='UTC')

start = canonicalize_datetime(start)
end = canonicalize_datetime(end)


weekends = rrule.rrule(
    rrule.YEARLY,
    byweekday=(rrule.SA, rrule.SU),
    cache=True,
    dtstart=start,
    until=end
    )

# New Year's Day
new_year = rrule.rrule(
    rrule.MONTHLY,
    byyearday=1,
    cache=True,
    dtstart=start,
    until=end
    )

# Easter Monday
easter_monday = rrule.rrule(
    rrule.DAILY,
    byeaster=1,
    cache=True,
    dtstart=start,
    until=end
    )

# Christi Himmelfahrt
ch_himm = rrule.rrule(
    rrule.DAILY,
    byeaster=39,
    cache=True,
    dtstart=pd.Timestamp('2013-01-01', tz='UTC'),
    until=pd.Timestamp('2013-12-31', tz='UTC')
    )

# Pfingstmontag
pfinst_mon = rrule.rrule(
    rrule.DAILY,
    byeaster=50,
    cache=True,
    dtstart=pd.Timestamp('2013-01-01', tz='UTC'),
    until=pd.Timestamp('2013-12-31', tz='UTC')
    )

# Labour Day (1st of May)
may_bank = rrule.rrule(
    rrule.MONTHLY,
    bymonth=5,
    bymonthday=1,
    cache=True,
    dtstart=start,
    until=end
    )

# Tag der Deutschen Einheit
tde = rrule.rrule(
    rrule.MONTHLY,
    bymonth=10,
    bymonthday=3,
    cache=True,
    dtstart=pd.Timestamp('2013-01-01', tz='UTC'),
    until=pd.Timestamp('2013-12-31', tz='UTC')
    )

# Christmas Eve
christmas_eve = rrule.rrule(
    rrule.MONTHLY,
    bymonth=12,
    bymonthday=24,
    cache=True,
    dtstart=start,
    until=end
)

# Christmas Day
christmas = rrule.rrule(
    rrule.MONTHLY,
    bymonth=12,
    bymonthday=25,
    cache=True,
    dtstart=start,
    until=end
)

# Boxing Day
boxing_day = rrule.rrule(
    rrule.MONTHLY,
    bymonth=12,
    bymonthday=26,
    cache=True,
    dtstart=start,
    until=end
)

# New Year's Eve
newyears_eve = rrule.rrule(
    rrule.MONTHLY,
    bymonth=12,
    bymonthday=31,
    cache=True,
    dtstart=start,
    until=end
    )
