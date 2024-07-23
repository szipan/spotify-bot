from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
prefs = {
    'profile.default_content_setting_values': {
        'images': 2
    }
}

chrome_options.add_experimental_option('prefs', prefs)
webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True
browser = webdriver.Chrome(options=chrome_options)
browser.get("https://open.spotify.com/")
print(f"Page Title: {browser.title}")

# Close the browser
browser.quit()
