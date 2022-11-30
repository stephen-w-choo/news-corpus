import pandas as pd
from datetime import datetime

dates = pd.date_range(start="2018-09-09",end="2018-10-02")

for date in dates:
    print(date.date())
    print(date.year)
    print(date.month)
    print(date.day)
