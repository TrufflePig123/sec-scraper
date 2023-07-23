from selenium import webdriver
from scraper.bot import SecBot



if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    bot = SecBot(options=options)
    bot.fetch_site()
    bot.lookup_ticker("ryam") #TODO, add input fields
    #bot.filter_annual_reports()