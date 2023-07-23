from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class SecBot(webdriver.Chrome):
    def __init__(self, options):
        super().__init__(options=options)
        self.implicitly_wait(5)

    def fetch_site(self):
        self.get("https://www.sec.gov/edgar/search/")
        #While we're at it, expand the search options tab
        expand_search_btn = self.find_element(By.ID, "show-full-search-form") #might be better in its own method for cleanliness, but its fine
        expand_search_btn.click()

    def set_ticker(self, ticker):
        ticker_search = self.find_element(By.ID, "entity-full-form")
        ticker_search.send_keys(ticker)

    def filter_filing_dates(self, date_from, date_to): #year, month day
        #Explicitly marking the date selector as a Select object allows us to switch between options using the option text value. 
        date_range_selector = Select(self.find_element(By.ID, "date-range-select"))
        date_range_selector.select_by_visible_text("Custom")
        
        date_from_search = self.find_element(By.ID, "date-from")
        #Data passed via send_keys() is overriden because the date fields are auto-filling inputs, hence the need for direct JavaScript assignment.
        self.execute_script("arguments[0].value = arguments[1];", date_from_search, date_from)
        date_to_search = self.find_element(By.ID ,"date-to")
        self.execute_script("arguments[0].value = arguments[1];", date_to_search, date_to)

    def filter_annual_reports(self):
        form_dropdown = self.find_element(By.ID, "form_filter")
        form_dropdown.click()

        annual_report_filter = self.find_element(By.CSS_SELECTOR, "a[data-filter-key='10-K']")
        annual_report_filter.click()

    def search(self):
        search = self.find_element(By.ID, "search")
        search.click()

