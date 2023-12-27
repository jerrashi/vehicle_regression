import sys
print(sys.executable)

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")

# Initialize WebDriver
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

# Get user input
'''
model = "Accord"
year = input("Enter model year: ")
trim = input("Enter car trim: ")
miles = input("Enter car miles: ")
'''


# Open the web page
driver.get("https://www.carfax.com/cars-for-sale")

# Wait for JavaScript to load
driver.implicitly_wait(10)  # Waits for 10 seconds

# Now you can parse the HTML content
html_content = driver.page_source
print(html_content)

# Locate the make dropdown and create a Select object
wait = WebDriverWait(driver, 10)  # Adjust the timeout as necessary
make_dropdown = wait.until(EC.presence_of_element_located((By.ID, "undefined-make-input")))
make_dropdown = Select(driver.find_element_by_id("undefined-make-input"))

# Retrieve and display all make options
print("Available Makes:")
make_options = [option.text for option in make_dropdown.options]
print(make_options)

# Get user input for make
make = input("Enter make: ")
while make not in make_options:
    print("ERROR - Invalid make")
    make = input("Enter make: ")

# Select the user make in order for web page to refresh
make_dropdown.select_by_visible_text(make)

# Locate the model dropdown and create a Select object
# Wait for the model dropdown to be populated
wait = WebDriverWait(driver, 10)  # Adjust the timeout as necessary
model_dropdown_id = "undefined-model-input"
wait.until(EC.presence_of_element_located((By.ID, model_dropdown_id)))
wait.until(lambda driver: Select(driver.find_element_by_id(model_dropdown_id)).options[1].text != "All Models")
model_dropdown = Select(driver.find_element_by_id(model_dropdown_id))

# Retrieve and display all model options
print("Available Models:")
model_options = [option.text for option in model_dropdown.options]
print(model_options)

# Function to enter user input into search options
def search_option(make, model, year, trim, miles):
   # Select the make based on user input
    make_dropdown.select_by_visible_text(make)

    # Locate the model dropdown and create a Select object
    model_dropdown = Select(driver.find_element_by_id("undefined-model-input"))

    # Now select the model
    model_dropdown = Select(driver.find_element_by_id(model_dropdown_id))
    model_dropdown.select_by_visible_text(model)