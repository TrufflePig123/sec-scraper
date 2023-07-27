import pandas as pd

class DataManager():
    '''Parses HTML tables and converts contents to pandas DataFrame objects.'''
    
    def __init__(self):
        pass

    def convert_to_df(self, table):
        html = table.get_attribute('outerHTML')
        df = pd.read_html(html)[0]

        print(df.columns)

