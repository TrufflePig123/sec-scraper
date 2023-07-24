from selenium import webdriver
from scraper.bot import SecBot
from selenium.webdriver.support.wait import WebDriverWait



if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    #options.add_argument("--window-size=2560,1440")

    bot = SecBot(options=options)
    bot.fetch_site()
    bot.set_ticker("ryam") #TODO, add input fields for ticker and filing date searches
    bot.filter_filing_dates("2015-07-23", "2023-07-23")
    bot.search()
    bot.filter_annual_reports()

    bot.refresh() #Refresh page to update the DOM once the filtered filing links are shown on the first page
    reports = bot.get_all_reports()

    for report in reports:
        report.click()
        bot.open_individual_document()

