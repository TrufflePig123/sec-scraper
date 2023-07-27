import pytest
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

driver = webdriver.Chrome()

@pytest.fixture
def balance():
    driver.get("https://www.sec.gov/Archives/edgar/data/1597672/000159767223000013/ryam-20221231.htm")

    row = driver.find_element(By.XPATH, '//span[text()="Assets"]')
    #Go up a certain number of parents
    balance_sheet = row.find_element(By.XPATH, "../../../..")

    return balance_sheet

def test_convert_to_df(balance):
    '''Test case messing around with converting + filtering balance sheet to dataframe'''
    html = balance.get_attribute('outerHTML')
    df = pd.read_html(html)[0]

    columns_with_value = df.columns[df.eq('2021').any()]
    df_filtered = df.drop(columns=columns_with_value)


    LOGGER.debug(df_filtered)
