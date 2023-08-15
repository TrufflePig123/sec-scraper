import pytest
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from functools import reduce
import logging
from scraper.bot import SecBot
from scraper.dfmanager import DataFrameManager

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

driver = webdriver.Chrome()






#@pytest.mark.parametrize('url', ) #TODO -- eventually itd be nice to parameritize some fixtures
#@pytest.fixture(scope="module", params=["https://www.sec.gov/Archives/edgar/data/1597672/000159767223000013/ryam-20221231.htm", "https://www.sec.gov/Archives/edgar/data/320193/000032019322000108/aapl-20220924.htm#ief5efb7a728d4285b6b4af1e880101bc_85", "https://www.sec.gov/Archives/edgar/data/1171759/000117175923000015/rrgb-20221225.htm#i19bc4ae4efae4be890587c34fd64d08e_79"])
@pytest.fixture
def balance():
    #driver.get("https://www.sec.gov/Archives/edgar/data/1597672/000159767223000013/ryam-20221231.htm") #ryam
    #driver.get("https://www.sec.gov/Archives/edgar/data/320193/000032019322000108/aapl-20220924.htm#ief5efb7a728d4285b6b4af1e880101bc_85") #appl
    driver.get("https://www.sec.gov/Archives/edgar/data/1171759/000117175923000015/rrgb-20221225.htm#i19bc4ae4efae4be890587c34fd64d08e_79") #rrgb

    #Using a wildcard because some tables may not use spans, but other things like </p> tags. Every balance sheet should have the phrase 'total assets' somewhere within it
    row = driver.find_element(By.XPATH, '//*[contains(text(), "Total assets")]') #TODO -- this will probably be what changes for each element, not the convert to df fn
    #BUG -- potential but, this function may not work if some sus company uses something like 'Total' to denote total assets/liabilitiesm maybe incorporate regex into here, but ik XPATH is funny with regex

    
    #Use xpath axis to find the nearest table. 
    #Parents directly preeceed elements. ex) <tr> <td>Data</td> </tr> <-- <tr> is the parent of td
    #Ancestors can be further up the tree. ex)  <table> <tbody> <td>Data</td> </tr> </tbody> </table> <-- <tr> is the parent, and <table>, <tbody> and <tr> are ancestors
    balance_sheet = row.find_element(By.XPATH, "./ancestor::table")

    #LOGGER.warning(balance_sheet.get_attribute("outerHTML"))

    return balance_sheet


def test_convert_to_df(balance):
    '''Test case messing around with converting + filtering balance sheet to dataframe'''
    html = balance.get_attribute('outerHTML')
    df = pd.read_html(html, displayed_only=False)[0]
    #Drop completely NaN columns
    df = df.dropna(axis=1, how="all")
    df = df[df.columns[:]].apply(str)

    df_final = pd.DataFrame(columns=["metric", "2022"]) #replace this with the current report year. This should be what gets returned (the final prod)

    df_final["metric"] = df[1]

    #columns_with_value = df.columns[df.eq('2021').any()]
    
    #recent_cols = df.columns[df.eq('2022').any()] #Searches for the EXACT str '2022' in the df...

    LOGGER.debug(df)

    def regex(column):
        #This regex searches for the substring 2022 within each column, except for when the str contains 'stock'
        #Sometimes companies place share change notices like "Common stock issued as of Dec 31 2022" in the sheet, and we want to ignore that #BUG pandas removes all commas/periods, so this regex expression might need some tweaking (could still detect 2022 inside the sheet data)
        
        
        return column.str.contains(r'^((?!stock).)*[^0-9]?2022') #TODO -- try to pick apart this regex


    most_recent_cols = df[df.columns[df.apply(regex).any()]]

    df_final["2022"] = most_recent_cols.iloc[:, 1] #This might cause bugs, but i think its okay


    LOGGER.debug(most_recent_cols)
    LOGGER.debug(df_final)


@pytest.fixture
def setup_statement_merge():
    '''Returns all scraped balance sheet instances in a list.'''
    dataframe_manager = DataFrameManager()
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    bot = SecBot(options=options)
    bot.get(f"https://www.sec.gov/edgar/search/#/dateRange=custom&entityName=aapl&startdt=2019-07-23&enddt=2023-07-23&filter_forms=10-K")

    reports = bot.get_all_reports()
    years = bot.get_year_range()

    all_balance_sheets = []

    for i in range(len(reports)):#FIXME: this loop crashes sometimes, need to find out why
        new_reports = bot.get_all_reports() #FIXME -- refactor this, this is a shoddy way of doing this
        report = new_reports[i]
        current_year = years[i]
        
        bot.open_individual_document(report) 
        #balance = bot.find_sheet(type="balance")
        balance = bot.find_balance_sheet()

        #FIXME: issue here is that the most recent filing was in 2022, but this shty loop looks for 2023, 2022, 2021, but theres no filings for 2023 yer
        #TODO might be better to just scrape the date off some eleement
        
        print(f'The current year is {current_year}')
        df_balance = dataframe_manager.convert_to_df(balance, current_year)

        all_balance_sheets.append(df_balance)

        #Go back to the reports
        bot.get(f"https://www.sec.gov/edgar/search/#/dateRange=custom&entityName=aapl&startdt=2019-07-23&enddt=2023-07-23&filter_forms=10-K")
    return all_balance_sheets 

def test_merge_all_statements(setup_statement_merge):
    all_statements = setup_statement_merge


    statements_merged = reduce(lambda left, right: pd.merge(left, right), all_statements)
    statements_merged = statements_merged.drop_duplicates() #TODO: need to drop the nan values here, but note that the nans are strings, so need to use drop()
    #df_base_year = all_statements[0]
    #for statement in all_statements[1:]:
     #   df_base_year.merge(statement) #THis returns something
    

    print(statements_merged)
    #LOGGER.debug(df_base_year)

    


    


