from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# Step 1: Parse the HTML File
with open("results.html", "r") as file:
    soup = BeautifulSoup(file, "lxml")

listings = []

# Base URL
base_url = "https://www.carfax.com"

# Step 2: Extract Information
for div in soup.find_all("div", class_="srp-listing-content"):
    for article in soup.find_all(lambda tag: tag.name == "article" and 
                                        tag.get("class", []) and 
                                        tag.get("class")[0].startswith("srp-list-item")):

        # Extract the VIN
        vin = article["data-vin"]
        # Locate the Header Tag and Extract Title and Link
        header = article.find("header", class_="srp-list-item__header")
        if header:
            link_tag = header.find("a", href=True)
            title = link_tag.get_text(strip=True)
            link = link_tag['href']
            # Concatenate with base URL if the link is relative
            if not link.startswith("http"):
                link = base_url + link
        else:
            title, link = None, None
            print("ERROR: no title or tag found")

        # Locate the Price Tag and Extract Price
        price_tag = article.find("div", class_="srp-list-item__price srp-list-item__section")
        if price_tag:
            price_tag = price_tag.get_text(strip=True).replace('Price:', '')
            if "$" in price_tag:
                price_tag = price_tag.split("$")
                price = price_tag[1]
            else:
                price = price_tag
        else:
            price = None
            print("ERROR: no price tag found")
        
        # Locate the Accident Tag and Extract Accident
        accident_tag = article.find("span", class_="srp-list-item--pillars-list-item search-result-list-item__no-accidents pillar-item__header")
        if accident_tag:
            condition = accident_tag.get_text(strip=True)
            if "accident" in condition.lower():
                if "no" in condition.lower():
                    has_accident = False
                else:
                    has_accident = True
            if "damage" in condition.lower():
                if "no" in condition.lower():
                    has_damage = False
                else:
                    has_damage = True
        else:
            condition = None
            has_accident, has_damage = False, False

        # Locate the Mileage Tag and Extract Mileage
        mileage = None
        for mileage_tag in article.find_all("span", class_="srp-list-item__basic-info-value"):
            if "Mileage" in mileage_tag:
                mileage = mileage_tag.get_text(strip=True).replace('Mileage: ', '')
            
        if mileage == None:
            print("ERROR: no mileage tag found")


        # Store the Extracted Information
        listing_info = {
            'VIN': vin,
            'Title': title,
            'Price': price,
            'Mileage': mileage,
            'Has_Accident': has_accident,
            'Has_Damage': has_damage,
            'Condition': condition
        }
        listings.append(listing_info)

# Now you have a list of dictionaries with each car's details
print(listings)

# Step 3: Run a linear regression on the data

# Step 4: Plot the data using plotly to generate an interactive scatterplot 
# visualization including line of best fit