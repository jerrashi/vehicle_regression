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
# chrome_options.add_argument("--headless")

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

# PART 1 - get user input and select options on page
def get_user_input():
    # Locate the make dropdown and create a Select object
    make_dropdown = Select(driver.find_element_by_id("undefined-make-input"))

    # Retrieve and display all make options
    print("Available Makes:")
    make_options = [option.text for option in make_dropdown.options]
    for i, value in enumerate(make_options):
        print(i + "." + " " + value)

    # Get user input for make
    make = input("Enter make index or name: ")
    while make not in make_options or make not in range(len(make_options)):
        print("ERROR - Invalid make")
        make = input("Enter make: ")

    # Select the user make in order for web page to refresh
    if make in make_options:
        make_dropdown.select_by_visible_text(make)
    else:
        make_dropdown.select_by_index(make)

    # Locate the model dropdown and get model options
    wait = WebDriverWait(driver, 10)  # Adjust the timeout as necessary
    model_dropdown_id = "undefined-model-input"
    wait.until(lambda driver: Select(driver.find_element_by_id(model_dropdown_id)).options[1].text != "All Models")
    model_dropdown = Select(driver.find_element_by_id(model_dropdown_id))

    # Retrieve and display all model options
    print("Available Models:")
    model_options = [option.text for option in model_dropdown.options]
    for i, value in enumerate(model_options):
        print(i + "." + " " + value)

    # Get user input for model
    model = input("Enter model index or name: ")
    while model not in model_options or model not in range(len(model_options)):
        print("ERROR - Invalid model")
        model = input("Enter model: ")

    # Select the user model in order for web page to refresh
    if model in model_options:
        model_dropdown.select_by_visible_text(model)
    else:
        model_dropdown.select_by_index(model)

    # Locate the more filters options and click it for year and trim options
    more_filters_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'More Filters')]")))
    more_filters_button.click()

    # Locate the year dropdown and input year options
    min_year_dropdown = Select(driver.find_element_by_id("min-year-input"))
    max_year_dropdown = Select(driver.find_element_by_id("max-year-input"))

    # Retrieve and display all year options
    print("Available Years:")
    min_year_options = [option.text for option in min_year_dropdown.options]
    for value in min_year_options:
        print(value)

    # Get user input for year
    min_year = input("Enter min year: ")
    while min_year not in min_year_options:
        print("ERROR - Invalid min year")
        min_year = input("Enter min year: ")
    max_year = input("Enter max year: ")
    while max_year not in min_year_options:
        print("ERROR - Invalid max year")
        max_year = input("Enter max year: ")

    # Select the user year in order for web page to refresh
    min_year_dropdown.select_by_visible_text(min_year)
    max_year_dropdown.select_by_visible_text(max_year)

    # Find all elements with an ID that includes the word "trim"
    trim_elements = driver.find_elements(By.XPATH, "//*[contains(@id,'trim')]")

    # Extract trim options
    available_trims = [element.text for element in trim_elements]
    print("Available Trims:")
    for trim in available_trims:
        print(trim)

    # Get user input for trim
    trim = input("Enter trim: ")
    while trim not in available_trims:
        print("ERROR - Invalid trim")
        trim = input("Enter trim: ")

    # Construct an XPath to find the checkbox based on the user's chosen trim
    xpath = f"//label[contains(text(), '{trim}')]/preceding-sibling::label[contains(@class, 'checkbox-input')]"

    # Find the checkbox element
    checkbox_element = driver.find_element(By.XPATH, xpath)

    # Click the checkbox
    checkbox_element.click()
    return make, model, min_year, max_year, trim

make, model, min_year, max_year, trim = get_user_input()

# PART 2 - Function to generate plot from filtered serach results
def plot_search_results():
    return