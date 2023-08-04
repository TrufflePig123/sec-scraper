from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import numpy as np


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
        reports = self.find_elements(By.XPATH, "//div[@id='hits']/descendant::a[@data-adsh]")
        
        return reports
    
       
    
    def open_individual_document(self, report_preview):
        report_preview.click()

        document_btn = self.find_element(By.ID, "open-file")
        
        #Naviagte to the document page
        self.get(document_btn.get_attribute("href"))

    def find_balance_sheet(self): #TODO: still not done with this man!!
        #The idea here is to look for certain keywords within all the tables the bot finds.
        #The more matches, the more likely it is that the candidate table is the actual balance sheet, and not some other table that just happens to match the text.
        key_metrics = ['total assets', 'total liabilities', 'cash and cash equivalents', 'inventories', 'accounts receivable'] #TODO: move this to the generic method
        all_candidate_tables = self.find_elements(By.XPATH, '//*[contains(text(), "Total assets")]/ancestor::table') #TODO
        table_match_counts = {} #TODO might want to put an if - else here to speed up even more


        #print(all_candidate_tables)
        for table in all_candidate_tables:
            descendants = table.find_elements(By.XPATH, './descendant::*') 

            #The call to list here slows things down significantly, but is essential for an accurate translation of the text values into a np array.
            descendant_text = np.array(list(map(lambda e: e.text.lower(), descendants))) #TODO -- try a way without calling list()

            mask = np.isin(descendant_text, key_metrics) 
            table_match_counts[descendant_text[mask].size] = table
            
        most_matches = max(table_match_counts.keys())

        sheet = table_match_counts[most_matches]

        #print(table_match_counts)
        
        return sheet

    def find_sheet(self, type): #TODO -- take the code from the test file and put it in here
        if type == "balance":
           #Using a wildcard because some tables may not use spans, but other things like </p> tags. Every balance sheet should have the phrase 'total assets' somewhere within it
            row = self.find_element(By.XPATH, '//*[contains(text(), "Total assets")]') #FIXME: Sometimes, 'Total assets' is part of another table, and it scrapes that instead. We need to find a way to put multipple identifying phrases of a balance sheet in here. Triggered by ticker='aapl'
        elif type == "cash_flow":               #FIXME: above xpath seems to be on the right track , but needs to be refined more..
            row = self.find_element(By.XPATH, '//*[contains(text(), "Total assets")]')  #FIXME: update these to contain identifing text
        elif type == "income":
            row = self.find_element(By.XPATH, '//*[contains(text(), "Total assets")]') 
        
        #Use xpath axis to find the nearest table
        sheet = row.find_element(By.XPATH, "./ancestor::table")



        return sheet
    
    def get_year_range(self):
        year_textboxes = self.find_elements(By.XPATH, "//td[@class='enddate']")

        year_range = [d.text[0:4] for d in year_textboxes]
        return year_range
    
