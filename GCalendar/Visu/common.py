
def prepare_data(data):
    data['day'] = data['StartTimeStamp'].apply(lambda x: str(x.day)+'/'+str(x.month))
    data['day_end'] = data['EndTimeStamp'].apply(lambda x: str(x.day)+'/'+str(x.month))
    data['duration'] = data['duration'].apply(lambda x: x.total_seconds()/3600)
    data['name_day'] = data['StartTimeStamp'].dt.strftime('%A')
    data['start_time'] = data['StartTimeStamp'].dt.strftime('%H') + ':' + data['StartTimeStamp'].dt.strftime('%M')
    data.sort_values(by='StartTimeStamp', inplace=True)
    return data