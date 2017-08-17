from datetime import datetime
from dateutil.parser import parse
import pandas as pd

war_start = '2011-01-03'

datetime.strptime(war_start, '%Y-%m-%d')

datetime.datetime(2011, 1, 3, 0, 0)

attack_dates = ['7/2/2011', '8/6/2012', '11/13/2013', '5/26/2011', '5/2/2001']

[datetime.strptime(x, '%m/%d/%Y') for x in attack_dates]

 parse(war_start)