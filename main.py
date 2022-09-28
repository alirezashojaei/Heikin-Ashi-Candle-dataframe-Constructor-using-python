import pandas as pd
import os
from datetime import datetime

# Loading the file.
# You can use any other methods of loading the data into Python 
# as long as that dataframe contains OPEN, HIGH, LOW, CLOSE columns 
# as that's required to calculate Heikin Ashi prices.
dataframe = pd.read_parquet('path/to/folder/dataframe.parquet')

#Let's look at the first 5 rows
dataframe.head()

#assigning existing columns to new variable HAdf
HAdf = dataframe[['open', 'high', 'low', 'close']]

# Calculating Heikin Ashi Close Price
# HAClose = (Open0 + High0 + Low0 + Close0)/4
HAdf['close'] = (dataframe['open'] + dataframe['high'] + dataframe['low'] + dataframe['close'])/4

# Calculating Heikin Ashi Open Price
# HAOpen = (HAOpen(-1) + HAClose(-1))/2
for i in range(len(dataframe)):
    if i == 0:
        HAdf.iat[0,0] = (dataframe['open'].iloc[0] + dataframe['close'].iloc[0])/2
    else:
        HAdf.iat[i,0] = (HAdf.iat[i-1,0] + HAdf.iat[i-1,3])/2

# Calculating Heikin Ashi High & Low Price
# High = MAX(High0, HAOpen0, HAClose0)
# Low = MIN(Low0, HAOpen0, HAClose0)
HAdf['high'] = HAdf.loc[:,['open', 'close']].join(dataframe['high']).max(axis=1)
HAdf['low'] = HAdf.loc[:,['open', 'close']].join(dataframe['low']).min(axis=1)
