

def write_gb(gb, name, year, df):
    with open(f'./Reports|2018-21/gb_{year}_{name}.txt', 'w') as f:
        df_string = gb.to_string()
        total_hours = df['Duration'].sum()
        f.write(f'Total records: {df.shape[0]} \n')
        f.write(f'Total hours: {total_hours} \n')
        f.write(df_string)


def set_name(word, col_width=60):
    if len(word) < col_width: word += ('_'*(col_width-len(word)))
    return word

def get_gb(data, cols, version, year, df):
    gbGeral = data[cols+['ColorsName','Name','Duration']].groupby(by=cols+['ColorsName','Name'])
    gb = gbGeral.sum()
    gb['Repeat'] = gbGeral.count()['Duration']
    gb.reset_index(inplace=True)
    gb = gb.sort_values(cols+['ColorsName','Repeat','Duration'], ascending=False)
    gb['Name'] = gb['Name'].apply(set_name)
    gb.set_index(cols+['ColorsName','Name'], inplace=True)
    write_gb(gb, version, year, df)

