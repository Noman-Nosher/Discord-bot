import discord
import random
import nest_asyncio
nest_asyncio.apply()
import gspread
import datetime
from datetime import date
import calendar
from datetime import datetime
import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from gspread_formatting.dataframe import format_with_dataframe


gc = gspread.service_account(filename ='credentials.json')
noman = gc.open_by_key('1du7kaTd12uO3qU6j6RPms1_14UJ_c300-g-7hu2E0nw')
noman_attend = noman.sheet1
import pandas as pd




df2 = get_as_dataframe(noman_attend)
print(df2.iloc[20,11])
