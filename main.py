from selenium import webdriver
from scraper.bot import SecBot
from scraper.dfmanager import DataFrameManager
from selenium.webdriver.support.wait import WebDriverWait

if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    #options.add_argument("--window-size=2560,1440")

    ticker = "aapl"
    start_date = "2015-07-23" #TODO, add input fields for ticker and filing date searches
    end_date = "2023-07-23"
    dataframe_manager = DataFrameManager()

    bot = SecBot(options=options)
    bot.fetch_site()
    bot.set_ticker(ticker) 
    bot.filter_filing_dates(start_date, end_date)
    bot.search()
    bot.filter_annual_reports()

    bot.refresh() #Refresh page to update the DOM once the filtered filing links are shown on the first page
    reports = bot.get_all_reports()
    years = bot.get_year_range()

    
    

    for i in range(len(reports)):
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

        #Go back to the reports
        bot.get(f"https://www.sec.gov/edgar/search/#/dateRange=custom&entityName={ticker}&startdt={start_date}&enddt={end_date}&filter_forms=10-K")
        
    

        print(df_balance)

    
    #TODO = Combine year-dfs into one consolidated balance sheet



