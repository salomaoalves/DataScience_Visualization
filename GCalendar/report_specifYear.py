import Analytics.agg_specifYear as agg
import constants as cts, data as data
import numpy as np

years = [2018, 2019, 2020, 2021]
for year in years:

    # Load data and create some cols
    df = data.get_data_by_year(data.read_db(), year)
    df['Duration'] = df['EndTimeStamp']-df['StartTimeStamp']
    df['DayByWeek'] = df['StartTimeStamp'].dt.weekday
    df['Weekend'] = np.where(df['DayByWeek'] > 5, True, False)
    df['ColorsName'] = [cts.colorId[str(c)][0] for c in df['Colors'].to_list()]
    df['Month'] = df['StartTimeStamp'].dt.month

    # Create Aggregations
    agg.get_gb(df, [], 'ForColors', year, df)
    agg.get_gb(df, ['Weekend'], 'InWeekends', year, df)
    agg.get_gb(df, ['Month'], 'ByMonth', year, df)
    agg.get_gb(df, ['DayByWeek'], 'ByDayOfWeek', year, df)



### Data Analysis - by myself
## 2018 - few things, only related to UFU (exams) and PET - with only one color (0)
## 2019 - more stuffs, but steal related to UFU (exams) and PET, but start to use  
##               differents colors and create Personal/Social Events
## 2020 - start to use a lot of events (increase 4x); in the 1 semester, more related with UFU/PET 
##               and Personal/Social Events, but more and specifics, like the UFU classes; 
##               in the 2 one, start to add work to; there is no pattern in the colors
## 2021 - increase amount of events (increase 3x); the events track is starting to getting good, but the
##               color pattern is not good, but better than last year, mainly in the second year half
## 2022 or later - the pattern is started to be used; normal report n visualization can be done