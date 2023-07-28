import pytest
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

driver = webdriver.Chrome()

#@pytest.mark.parametrize('url', )
#@pytest.fixture(scope="module", params=["https://www.sec.gov/Archives/edgar/data/1597672/000159767223000013/ryam-20221231.htm", "https://www.sec.gov/Archives/edgar/data/320193/000032019322000108/aapl-20220924.htm#ief5efb7a728d4285b6b4af1e880101bc_85", "https://www.sec.gov/Archives/edgar/data/1171759/000117175923000015/rrgb-20221225.htm#i19bc4ae4efae4be890587c34fd64d08e_79"])
@pytest.fixture
def balance():
    driver.get("https://www.sec.gov/Archives/edgar/data/1597672/000159767223000013/ryam-20221231.htm") #ryam
    #driver.get("https://www.sec.gov/Archives/edgar/data/320193/000032019322000108/aapl-20220924.htm#ief5efb7a728d4285b6b4af1e880101bc_85") #appl
    #driver.get("https://www.sec.gov/Archives/edgar/data/1171759/000117175923000015/rrgb-20221225.htm#i19bc4ae4efae4be890587c34fd64d08e_79") #rrgb

    #Using a wildcard because some tables may not use spans, but other things like </p> tags. Every balance sheet will have current assets as something.
    row = driver.find_element(By.XPATH, '//*[contains(text(), "Total assets")]') #FIXME

    
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

    df_final = pd.DataFrame(columns=["metric", 2022]) #replace this with the current report year. This should be what gets returned (the final prod)

    df_final["metric"] = df[1]

    columns_with_value = df.columns[df.eq('2021').any()]
    
    recent_cols = df.columns[df.eq('2022').any()]

    #df_filtered = df.drop(columns=columns_with_value)

    #LOGGER.info(recent_cols) #cols 3, 4, 5 contain str 2022

    LOGGER.debug(df)

    LOGGER.debug(df[[3, 4, 5]]) # displays html columns with the year 2022

    LOGGER.debug(df_final)


