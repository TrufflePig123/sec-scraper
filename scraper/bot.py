from selenium import webdriver

class SecBot(webdriver.Chrome):
    def __init__(self, options):
        super().__init__(options=options)
        self.implicitly_wait(5)

    def fetch_site(self):
        self.get("https://www.sec.gov/edgar/search/")
        #While we're at it, expand the search options tab
        expand_search_btn = self.find_element("id", "show-full-search-form") #might be better in its own method for cleanliness, but its fine
        expand_search_btn.click()

    def lookup_ticker(self, ticker):
        ticker_search = self.find_element("id", "entity-full-form")
        ticker_search.send_keys(ticker)

    def filter_annual_reports(self):
        filings_button = self.find_element("id", "show-filing-types")
        filings_button.click()

        annual_report_box = self.find_element("css_selector", "::before")
        #annual_report_box = self.find_element("id", "fcb14")
        annual_report_box.click()

    

