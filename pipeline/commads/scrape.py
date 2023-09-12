from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Selenium browser settings
# selenium_web_browser = os.getenv("USE_WEB_BROWSER", "chrome")
# selenium_headless = os.getenv("HEADLESS_BROWSER", "True") == "True"

def scrape_text_with_selenium(url: str) -> str:
#     """Scrape text from a website using selenium

#     Args:
#         url (str): The url of the website to scrape

#     Returns:
#         str: The text scraped from the website
#     """
#     logging.getLogger("selenium").setLevel(logging.CRITICAL)

#     options_available = {
#         "chrome": ChromeOptions,
#         "safari": SafariOptions,
#         "firefox": FirefoxOptions,
#         "edge": EdgeOptions,
#     }

#     options = options_available[selenium_web_browser]()
#     options.add_argument(
#         "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.49 Safari/537.36"
#     )

#     if selenium_web_browser == "firefox":
#         if selenium_headless:
#             options.headless = True
#             options.add_argument("--disable-gpu")
#         driver = webdriver.Firefox(
#             executable_path=GeckoDriverManager().install(), options=options
#         )
#     elif selenium_web_browser == "safari":
#         # Requires a bit more setup on the users end
#         # See https://developer.apple.com/documentation/webkit/testing_with_webdriver_in_safari
#         driver = webdriver.Safari(options=options)
#     elif selenium_web_browser == "edge":
#         driver = webdriver.Edge(
#             executable_path=EdgeChromiumDriverManager().install(), options=options
#         )
#     else:
#         # if platform == "linux" or platform == "linux2":
#         #     options.add_argument("--disable-dev-shm-usage")
#         #     options.add_argument("--remote-debugging-port=9222")

#         options.add_argument("--no-sandbox")
#         if selenium_headless:
#             options.add_argument("--headless=new")
#             options.add_argument("--disable-gpu")

#         # chromium_driver_path = Path(".")

#         driver = webdriver.Chrome()
#         #     executable_path=chromium_driver_path
#         #     if chromium_driver_path.exists()
#         #     else ChromeDriverManager().install(),
#         #     options=options,
#         # )
    driver = webdriver.Chrome()
    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Get the HTML content directly from the browser's DOM
    page_source = driver.execute_script("return document.body.outerHTML;")
    soup = BeautifulSoup(page_source, "html.parser")

    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = "\n".join(chunk for chunk in chunks if chunk)
    return text


# text = scrape_text_with_selenium("https://money.cnn.com/quote/forecast/forecast.html?symb=NVDA")[1]