import pandas as pd

class DataFrameManager():
    '''Parses, modifies, and manipulates HTML tables from the annual reports and DataFrame objects, organizing them into a yearly picture of a company's financials.'''
    
    def __init__(self):
        pass

    def convert_to_df(self, table, year: str):
        '''Parses HTML tables and converts contents to pandas DataFrame objects.'''

        html = table.get_attribute('outerHTML')

        df = pd.read_html(html)[0] #FIXME For some reason, this only scrapes half the table on certain situations??

        #Drop completely NaN columns
        df = df.dropna(axis=1, how="all")

        df = df.applymap(str)

        df_final = pd.DataFrame(columns=["Metric", year]) 

        #print(df)
        #mask = df.isin(['Total assets'])

        metric_columns = df.columns[df.apply(lambda x: x == 'Total assets').any()].to_numpy() #BUG -- this might return a list of cols if read_html scrapes the metric column multiple times
        metric_column = metric_columns[0]
        #print(metric_column)

        

        def regex(column):
            #This regex searches for the substring 2022 within each column, except for when the str contains 'stock'
            #Sometimes companies place share change notices like "Common stock issued as of Dec 31 2022" in the sheet, and we want to ignore that 
            return column.str.contains(fr'^((?!stock).)*[^0-9]?{year}') #BUG pandas removes all commas/periods, so this regex expression might need some tweaking (could still detect 2022 inside the sheet data)


        most_recent_cols = df[df.columns[df.apply(regex).any()]]

        #print(most_recent_cols)

        mask = most_recent_cols.apply(lambda col: col.str.contains(r'[0-9]'))
        numerical_data = df[mask.apply(lambda col: col.value_counts().get(True)).idxmax()]

        #print(numerical_data)

        
            
        #num_col = numerical_data.applymap(assert_num)

        #print(num_col)
        #print(metric_column)
        df_final["Metric"] = df[metric_column]
        df_final[year] = numerical_data
        #df_final[year] = most_recent_cols.iloc[:, 1]  #BUG: this key could pose an issue if for example, the parser grabs 4 'most recent' cols instead of the expected 3.

        print(df_final)

        return df_final

