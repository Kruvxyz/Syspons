from pipeline.commads.scrape import scrape_text_with_selenium

#fixme(guyhod): add CommandRegistry [The CommandRegistry class is a manager for a collection of Command objects.]
commands = {"scrape": [
    "Scrape text from a website using selenium",
    "Args: <url(str): The url of the website to scrape>",
    "Returns: str: The text scraped from the website",
    scrape_text_with_selenium
]}
