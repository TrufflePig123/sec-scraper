from selenium import webdriver
from scraper.bot import SecBot



if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    bot = SecBot(options=options)
    bot.fetch_site()
    bot.set_ticker("ryam") #TODO, add input fields for ticker and filing date searches
    bot.filter_filing_dates("2015-07-23", "2023-07-23")
    bot.search()
    bot.filter_annual_reports()