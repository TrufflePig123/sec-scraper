import pandas as pd

class DataManager():
    '''Parses HTML tables and converts contents to pandas DataFrame objects.'''
    
    def __init__(self):
        pass

    def convert_to_df(self, table):
        html = table.get_attribute('outerHTML')
        df = pd.read_html(html)[0]

        #Drop completely NaN columns
        df = df.dropna(axis=1, how="all")

        df_final = pd.DataFrame(columns=["Metric", "2022"]) #replace this with the current report year. This should be what gets returned (the final prod)
        df_final["Metric"] = df[1]

        def regex(column):
            #This regex searches for the substring 2022 within each column, except for when the str contains 'stock'
            #Sometimes companies place share change notices like "Common stock issued as of Dec 31 2022" in the sheet, and we want to ignore that 
            return column.str.contains(r'^((?!stock).)*[^0-9]?2022') #BUG pandas removes all commas/periods, so this regex expression might need some tweaking (could still detect 2022 inside the sheet data)

        most_recent_cols = df[df.columns[df.apply(regex).any()]]
        df_final["2022"] = most_recent_cols.iloc[:, 1] 

        return df_final

