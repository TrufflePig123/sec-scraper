import pandas as pd

class DataFrameManager():
    '''Parses, modifies, and manipulates HTML tables from the annual reports and DataFrame objects, organizing them into a yearly picture of a company's financials.'''
    
    def __init__(self):
        pass

    def convert_to_df(self, table, year: str):
        '''Parses HTML tables and converts contents to pandas DataFrame objects.'''

        html = table.get_attribute('outerHTML')

        testlist = pd.read_html(html)
        df = pd.read_html(html)[0] #FIXME For some reason, this only scrapes half the table on certain situations??

       

        #Drop completely NaN columns
        df = df.dropna(axis=1, how="all")

        df_final = pd.DataFrame(columns=["Metric", year]) #FIXME replace this with the current report year. This should be what gets returned (the final prod)
        df_final["Metric"] = df[1]

        def regex(column):
            #This regex searches for the substring 2022 within each column, except for when the str contains 'stock'
            #Sometimes companies place share change notices like "Common stock issued as of Dec 31 2022" in the sheet, and we want to ignore that 
            return column.str.contains(fr'^((?!stock).)*[^0-9]?{year}') #BUG pandas removes all commas/periods, so this regex expression might need some tweaking (could still detect 2022 inside the sheet data)
            #TODO -- replace regex with the current year

        most_recent_cols = df[df.columns[df.apply(regex).any()]]

        #print(most_recent_cols)

        df_final[year] = most_recent_cols.iloc[:, 1] 

        return df_final

