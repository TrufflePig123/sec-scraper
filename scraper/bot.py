from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class SecBot(webdriver.Chrome):
    def __init__(self, options):
        super().__init__(options=options)
        self.implicitly_wait(10)

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

    def get_all_reports(self):
        reports = self.find_element(By.CSS_SELECTOR, "a[data-adsh='0001597672-23-000013']") #TODO -- for later, grab all the report </a> tags and return them
        
        return [reports]
    
    def open_individual_document(self, report_preview):
        report_preview.click()

        document_btn = self.find_element(By.ID, "open-file")
        
        #Naviagte to the document page
        self.get(document_btn.get_attribute("href"))


    def find_sheet(self, type): #TODO -- take the code from the test file and put it in here
        
        if type == "balance":
           #Using a wildcard because some tables may not use spans, but other things like </p> tags. Every balance sheet should have the phrase 'total assets' somewhere within it
            row = self.find_element(By.XPATH, f'//*[contains(text(), "Total assets")]') 
        elif type == "cash_flow":
            row = self.find_element(By.XPATH, f'//*[contains(text(), "Total assets")]')  #TODO: update these to contain identifing text
        elif type == "income":
            row = self.find_element(By.XPATH, f'//*[contains(text(), "Total assets")]') 
        
        #Use xpath axis to find the nearest table
        balance_sheet = row.find_element(By.XPATH, "./ancestor::table")

        return balance_sheet


    
    


